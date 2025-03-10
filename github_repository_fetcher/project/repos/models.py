from django.db import models


class FetchJob(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_repos = models.IntegerField()
    repos_fetched = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    error_message = models.TextField(blank=True, null=True)


class Repository(models.Model):
    github_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    stars = models.IntegerField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["stars"]),
            models.Index(fields=["fetched_at"]),
        ]


class Tag(models.Model):
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ["repository", "name"]
