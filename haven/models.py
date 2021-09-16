from django.db import models

# Create your models here.

class PortTemplate(models.Model):
    arkitekt_id = models.CharField(max_length=1000, help_text="The corresponding Template on the Arkitekt Instance")
    namespace = models.CharField(max_length=100, help_text="Corresponds to docker hub user")
    repo = models.CharField(max_length=100, help_text="Corresponds to docker repo name")
    tag = models.CharField(max_length=100, help_text="Corresponds to docker hub user")
    env = models.JSONField(help_text="Environment parameters for the Port", null=True)

    def __str__(self) -> str:
        return f"Docker container {self.namespace}/{self.repo}:{self.tag} on Arkitekt {self.arkitekt_id}"


class PortPod(models.Model):
    arkitekt_id = models.CharField(max_length=1000, help_text="The Corresponding Pod on the Arkitekt Instance")
    template = models.ForeignKey(PortTemplate, help_text="The corresponding Template", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="The containers clear-text name")


    def __str__(self) -> str:
        return f"Running Docker container for {self.template}"

