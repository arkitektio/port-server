from django.db import models
from django.contrib.auth import get_user_model
from haven.enums import WhaleRuntime
from haven.storage import PrivateMediaStorage
import uuid

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

    def __str__(self):
        return f"{self.user}/{self.repo}:{self.branch}"

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


class Manifest(models.Model):
    version = models.CharField(max_length=400)
    identifier = models.CharField(max_length=4000)
    scopes = models.JSONField(default=list)
    requirements = models.JSONField(default=list)
    logo = models.ImageField(
        max_length=1000, null=True, blank=True, storage=PrivateMediaStorage()
    )
    original_logo = models.CharField(
        max_length=1000, null=True, blank=True, help_text="The original logo url"
    )
    entrypoint = models.CharField(max_length=4000, default="app")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "version"], name="unique_manifest for version"
            )
        ]


class Deployment(models.Model):
    deployment_id = models.CharField(max_length=400, unique=True, default=uuid.uuid4)
    build_id = models.CharField(max_length=400, default=uuid.uuid4)
    manifest = models.ForeignKey(
        Manifest, on_delete=models.CASCADE, related_name="deployments"
    )
    repo = models.ForeignKey(
        GithubRepo, on_delete=models.CASCADE, related_name="deployments"
    )
    image = models.CharField(max_length=400, default="jhnnsrs/fake:latest")
    builder = models.CharField(max_length=400)
    definitions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now=True)
    deployed_at = models.DateTimeField(null=True)

    def __str__(self):
        return ""

    class Meta:
        ordering = ["-created_at"]
