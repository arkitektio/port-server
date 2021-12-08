from django.db import models

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
    branch = models.CharField(max_length=4000)
    definition = models.JSONField(
        default=dict, help_text="The Node this Repo wants to define"
    )
    backend = models.BooleanField(
        default=False, help_text="Does this Task want to be a BackendApp?"
    )
    scopes = models.JSONField(default=list)
    image = models.CharField(max_length=400, default="jhnnsrs/ome:latest")
    whale = models.OneToOneField(
        Whale, null=True, blank=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now=True)
