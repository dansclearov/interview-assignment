import time
from celery import shared_task
from django.db import transaction
from django.conf import settings
from .models import FetchJob, Repository, Tag
from .github_client import GitHubGraphQLClient


@shared_task
def fetch_repos_task(count, job_id):
    job = FetchJob.objects.get(id=job_id)
    job.status = "PROCESSING"
    job.save()

    try:
        client = GitHubGraphQLClient()

        per_batch = 100
        total_fetched = 0
        cursor = None

        while total_fetched < count:
            if client.rate_limit_remaining < 100:
                current_time = time.time()
                wait_time = max(0, client.rate_limit_reset - current_time) + 10
                if wait_time > 0:
                    time.sleep(wait_time)
            query = """
            query($cursor: String, $count: Int!) {
              search(query: "stars:>1", type: REPOSITORY, first: $count, after: $cursor) {
                pageInfo { endCursor hasNextPage }
                nodes {
                  ... on Repository {
                    id
                    name
                    url
                    stargazerCount
                    refs(refPrefix: "refs/tags/", first: 10) {
                      nodes { name }
                    }
                  }
                }
              }
            }
            """

            result = client.execute(
                query,
                {"cursor": cursor, "count": min(per_batch, count - total_fetched)},
            )

            with transaction.atomic():
                for repo_data in result["data"]["search"]["nodes"]:
                    repo, created = Repository.objects.update_or_create(
                        github_id=repo_data["id"],
                        defaults={
                            "name": repo_data["name"],
                            "url": repo_data["url"],
                            "stars": repo_data["stargazerCount"],
                        },
                    )

                    tag_objects = []
                    for tag in repo_data["refs"]["nodes"]:
                        tag_objects.append(Tag(repository=repo, name=tag["name"]))

                    Tag.objects.bulk_create(tag_objects)

            total_fetched += len(result["data"]["search"]["nodes"])
            cursor = result["data"]["search"]["pageInfo"]["endCursor"]

            job.repos_fetched = total_fetched
            job.save()

            if not result["data"]["search"]["pageInfo"]["hasNextPage"]:
                break

        job.status = "COMPLETED"
        job.save()
    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        job.save()
        raise
