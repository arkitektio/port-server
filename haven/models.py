from django.db import models
from django.contrib.auth import get_user_model
from haven.enums import WhaleRuntime

# Create your models here.



class Whale(models.Model):
    image = models.CharField(max_length=4000)
    config = models.JSONField(
        help_text="Environment parameters for the Port", null=True
    )
    client_id = models.CharField(max_length=1000, unique=True)
    client_secret = models.CharField(max_length=1000)
    scopes = models.JSONField()
    url = models.CharField(max_length=1000)
    runtime = models.CharField(
        max_length=1000,
        null=True,
        choices=WhaleRuntime.choices,
        default=WhaleRuntime.RUNC.value,
    )
    version = models.CharField(max_length=1000)
    identifier = models.CharField(max_length=1000)


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


class RepoScan(models.Model):
    name = models.CharField(max_length=4000)
    repo = models.ForeignKey(GithubRepo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=400, default="jhnnsrs/ome:latest")
    version = models.CharField(max_length=400, default="latests")
    identifier = models.CharField(max_length=4000)
    scopes = models.JSONField()

    def __str__(self):
        return f"Scan of {self.repo} at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "version"], name="unique_repo_scan"
            )
        ]
