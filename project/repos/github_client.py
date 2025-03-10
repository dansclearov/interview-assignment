import requests
from django.conf import settings


class GitHubGraphQLClient:
    def __init__(self, token=None):
        self.token = token or settings.GITHUB_TOKEN
        self.endpoint = "https://api.github.com/graphql"
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = 0

    def execute(self, query, variables=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload = {"query": query, "variables": variables or {}}

        response = requests.post(self.endpoint, json=payload, headers=headers)

        if "X-RateLimit-Remaining" in response.headers:
            self.rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in response.headers:
            self.rate_limit_reset = int(response.headers["X-RateLimit-Reset"])

        if response.status_code != 200:
            raise Exception(f"GraphQL request failed: {response.text}")

        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL query error: {result['errors']}")

        return result
