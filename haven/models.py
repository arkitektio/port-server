from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Whale(models.Model):
    template = models.CharField(
        max_length=1000,
        help_text="The corresponding Template on the Arkitekt Instance",
        unique=True,
    )
    image = models.CharField(max_length=4000)
    config = models.JSONField(
        help_text="Environment parameters for the Port", null=True
    )

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Docker container {self.namespace}/{self.repo}:{self.tag} on Arkitekt {self.template}"


class GithubRepo(models.Model):
    repo = models.CharField(max_length=4000)
    user = models.CharField(max_length=4000)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    branch = models.CharField(max_length=4000)
    image = models.CharField(max_length=400, default="jhnnsrs/ome:latest")
    created_at = models.DateTimeField(auto_now=True)
