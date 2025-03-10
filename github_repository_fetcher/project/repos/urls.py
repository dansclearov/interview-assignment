from django.urls import path
from . import views

urlpatterns = [
    path("api/repositories/fetch", views.fetch_repositories, name="fetch_repositories"),
    path("api/jobs/<int:job_id>/status", views.job_status, name="job_status"),
    path("api/repositories", views.list_repositories, name="list_repositories"),
    path("api/repositories/<int:repo_id>", views.get_repository, name="get_repository"),
]
