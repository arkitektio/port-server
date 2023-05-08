from django.db.models import TextChoices
from balder.enum import InputEnum
import graphene


class WhaleRuntime(TextChoices):
    """Docker runtime."""

    NVIDIA = "nvidia", "NVIDIA"
    RUNC = "runc", "RunC"


WhaleRuntimeInput = InputEnum.from_choices(WhaleRuntime)


class DockerRuntime(graphene.Enum):
    """Docker runtime."""

    NVIDIA = "nvidia"
    RUNC = "runc"


class ContainerStatus(graphene.Enum):
    CREATED = "created"
    RESTARTING = "restarting"
    RUNNING = "running"
    REMOVING = "removing"
    PAUSED = "paused"
    EXITED = "exited"
    DEAD = "dead"


class PullProgressStatus(graphene.Enum):
    """Docker pull progress status."""
    PULLING = "Pulling"
    PULLED = "Pulled"

class UpProgressStatus(graphene.Enum):
    """Docker pull progress status."""
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    DONE = "done"