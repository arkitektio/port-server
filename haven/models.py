from django.db import models
from django.contrib.auth import get_user_model
from haven.enums import WhaleRuntime

# Create your models here.


class Whale(models.Model):
    deployment = models.ForeignKey(
        "Deployment",
        on_delete=models.CASCADE,
        related_name="whales",
    )
    url = models.CharField(max_length=1000)
    client_id = models.CharField(max_length=1000)
    token = models.CharField(max_length=10000, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class GithubRepo(models.Model):
    repo = models.CharField(max_length=4000)
    user = models.CharField(max_length=4000)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    branch = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def pyproject_url(self):
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/pyproject.toml"

    @property
    def readme_url(self):
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/README.md"

    @property
    def manifest_url(self):
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/.arkitekt/manifest.yaml"

    @property
    def deployments_url(self):
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/.arkitekt/deployments.yaml"


class Deployment(models.Model):
    version = models.CharField(max_length=400, default="latests")
    identifier = models.CharField(max_length=4000)
    scopes = models.JSONField(default=list)
    requirements = models.JSONField(default=list)
    repo = models.ForeignKey(
        GithubRepo, on_delete=models.CASCADE, related_name="deployments", null=True
    )
    created_at = models.DateTimeField(auto_now=True)
    deployed_at = models.DateTimeField(auto_now=True)
    command = models.CharField(max_length=4000, null=True, default="arkitekt run port")
    image = models.CharField(max_length=400)
    entrypoint = models.CharField(max_length=4000, default="app")

    def __str__(self):
        return f"Deployment at {self.repo} at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "version"], name="unique_deployment for version"
            )
        ]
