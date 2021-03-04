from django.db import models

# Create your models here.

class PortTemplate(models.Model):
    arkitekt_id = models.CharField(max_length=1000, help_text="The corresponding Template on the Arkitekt Instance")
    namespace = models.CharField(max_length=100, help_text="Corresponds to docker hub user")
    repo = models.CharField(max_length=100, help_text="Corresponds to docker repo name")
    tag = models.CharField(max_length=100, help_text="Corresponds to docker hub user")
    env = models.JSONField(help_text="Environment parameters for the Port", null=True)


    class Meta:
        arnheim = True

    def __str__(self) -> str:
        return f"Docker container {self.namespace}/{self.repo}:{self.tag} on Arkitekt {self.arkitekt_id}"



class ProviderChannel(models.Model):
    arkitekt_id = models.CharField(max_length=1000, help_text="The corresponding Provider on the Arkitekt Instance")
    channel = models.CharField(max_length=1000, help_text="The channel we  will listen to")

    def __str__(self) -> str:
        return f"The channels we are listening to"