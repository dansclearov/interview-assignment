import json
import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import FetchJob, Repository
from .tasks import fetch_repos_task


STORAGE_DIR = os.path.join(settings.BASE_DIR, "repository_data")
os.makedirs(STORAGE_DIR, exist_ok=True)


@csrf_exempt
@require_http_methods(["POST"])
def fetch_repositories(request):
    try:
        data = json.loads(request.body)
        count = int(data.get("count", 10))

        if count <= 0:
            return JsonResponse(
                {"status": "error", "message": "Count must be positive"}, status=400
            )

        job = FetchJob.objects.create(total_repos=count, status="PENDING")

        fetch_repos_task.delay(count, job.id)

        return JsonResponse(
            {
                "status": "accepted",
                "message": f"Scheduled fetch of {count} repositories",
                "job_id": job.id,
                "status_url": f"/api/jobs/{job.id}/status",
            }
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@require_http_methods(["GET"])
def job_status(request, job_id):
    try:
        job = FetchJob.objects.get(id=job_id)

        return JsonResponse(
            {
                "status": job.status,
                "total_repos": job.total_repos,
                "repos_fetched": job.repos_fetched,
                "progress_percentage": round(
                    (job.repos_fetched / job.total_repos) * 100, 2
                )
                if job.total_repos > 0
                else 0,
                "error": job.error_message,
                "created_at": job.created_at.isoformat(),
                "updated_at": job.updated_at.isoformat(),
            }
        )
    except FetchJob.DoesNotExist:
        return


@require_http_methods(["GET"])
def list_repositories(request):
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 20))
    offset = (page - 1) * page_size

    total_repos = Repository.objects.count()

    repositories = Repository.objects.order_by("-stars")[offset : offset + page_size]

    repos_data = [
        {
            "id": repo.id,
            "name": repo.name,
            "url": repo.url,
            "stars": repo.stars,
            "fetched_at": repo.fetched_at.isoformat(),
        }
        for repo in repositories
    ]

    return JsonResponse(
        {
            "total": total_repos,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_repos + page_size - 1) // page_size,
            "repositories": repos_data,
        }
    )


@require_http_methods(["GET"])
def get_repository(request, repo_id):
    try:
        repo = Repository.objects.get(id=repo_id)
        tags = list(repo.tags.values_list("name", flat=True))

        return JsonResponse(
            {
                "id": repo.id,
                "name": repo.name,
                "url": repo.url,
                "stars": repo.stars,
                "tags": tags,
                "fetched_at": repo.fetched_at.isoformat(),
            }
        )
    except Repository.DoesNotExist:
        return JsonResponse({"error": "Repository not found"}, status=404)
