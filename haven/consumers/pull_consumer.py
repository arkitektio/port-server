from channels.consumer import SyncConsumer
from haven.client import api, get_my_networks
from haven.models import Whale, Manifest
from haven.graphql.subscriptions.whale import WhaleUpdateSubscription
from haven.graphql.subscriptions.container import ContainerUpdateSubscription
import docker
from django.conf import settings
import logging

DOWNLOAD_STATUS = "Downloading"
EXTRACTING_STATUS = "Extracting"
PULL_COMPLETE = "Pull complete"
DOWNLOAD_COMPLETE = "Download complete"
PULLED = "Pulled"
WAITING = "Waiting"


logger = logging.getLogger(__name__)


class DockerApiConsumer(SyncConsumer):
    def pull_image(self, whale: Whale):
        logger.info("Pulling Image: " + whale.deployment.image)
        s = api.api.pull(whale.deployment.image, stream=True, decode=True)

        keeping_progress = []
        finished = []

        WhaleUpdateSubscription.broadcast(
            {"whale": whale.id, "pull": {"status": "Pulling", "progress": 0.5}},
            [
                WhaleUpdateSubscription.WHALEID_GROUP(whale.id),
                WhaleUpdateSubscription.USERID_GROUP(whale.creator.id),
            ],
        )

        for f in s:
            if "status" in f:
                logger.info(f["status"])
                if f["status"] in [WAITING]:
                    keeping_progress.append(f["id"])

                if f["status"] in [PULL_COMPLETE]:
                    if f["id"] in keeping_progress:
                        finished.append(f["id"])

                    progress = len(finished) / (
                        len(keeping_progress) if len(keeping_progress) > 0 else 1
                    )

                    logger.info(
                        "Progress: " + whale.deployment.image + " " + str(progress)
                    )

                    WhaleUpdateSubscription.broadcast(
                        {
                            "whale": whale.id,
                            "pull": {"status": "Pulling", "progress": progress},
                        },
                        [
                            WhaleUpdateSubscription.WHALEID_GROUP(whale.id),
                            WhaleUpdateSubscription.USERID_GROUP(whale.creator.id),
                        ],
                    )

        WhaleUpdateSubscription.broadcast(
            {"whale": whale.id, "pull": {"status": PULLED, "progress": 1}},
            [
                WhaleUpdateSubscription.WHALEID_GROUP(whale.id),
                WhaleUpdateSubscription.USERID_GROUP(whale.creator.id),
            ],
        )

    def pull_whale(self, message):
        whale_id = message["whale"]
        whale = Whale.objects.get(id=whale_id)

        self.pull_image(whale)

    def up_whale(self, message):
        whale_id = message["whale"]
        instance = message["instance"]
        network = message["network"]
        whale = Whale.objects.get(id=whale_id)
        logger.info("Deploying Image: " + whale.deployment.image)

        x = None

        try:
            x = api.images.get(whale.deployment.image)  # Check if image exists
        except Exception as e:
            logger.info("Image Not found " + whale.deployment.image)
            print("Whale Not pulled yet.. pulling: " + str(whale_id) + " " + str(e))

        if x is None:
            logger.info("Didn`t found image: " + whale.deployment.image)
            self.pull_image(whale)

        logger.info("Has Image " + (str(x)))

        manifest: Manifest = whale.deployment.manifest

        requirements = manifest.requirements

        if "gpu" in requirements:
            device_requests = [
                docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
            ]
        else:
            device_requests = None

        print("Up Whale")

        network = network or get_my_networks()[0].id

        command = f"arkitekt run prod -b {whale.deployment.builder} -i {instance} -t {whale.token} --url {whale.url}"
        print(command)
        try:
            container = api.containers.get(f"{whale.id}-{instance}")
            print(f"Container {container} Exists, doing nothing")
        except docker.errors.NotFound:
            container = api.containers.run(
                whale.deployment.image,
                command=command,
                detach=True,
                name=f"{whale.id}-{instance}",
                labels={
                    "whale": f"{whale.id}",
                    "instance": f"{instance}",
                    "host": f"{settings.DOCK['HOST']}",
                },
                restart_policy={"Name": "on-failure", "MaximumRetryCount": 5},
                device_requests=device_requests,
                environment={
                    "FAKTS_URL": whale.url,
                    "FAKTS_TOKEN": whale.token,
                    "REKUEST_INSTANCE": instance,
                },
                network=network,
            )
            print(
                "Container Started: "
                + str(message["whale"])
                + "-"
                + str(message["instance"])
            )

        WhaleUpdateSubscription.broadcast(
            {
                "whale": whale_id,
                "up": {"instance": instance, "container": container.id},
            },
            [
                WhaleUpdateSubscription.WHALEID_GROUP(whale_id),
                WhaleUpdateSubscription.USERID_GROUP(whale.creator.id),
            ],
        )

    def restart_container(self, message):
        container = api.containers.get(message["container"])

        s = container.restart()
        print("Container Restarted: " + message["container"])

    def stop_container(self, message):
        container = api.containers.get(message["container"])

        s = container.stop()
        print("Container Stopped: " + message["container"])

    def remove_container(self, message):
        container = api.containers.get(message["container"])

        s = container.remove()
        print("Container Removed: " + message["container"])
