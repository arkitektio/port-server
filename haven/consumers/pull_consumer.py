from channels.consumer import SyncConsumer
from haven.client import api
from haven.models import Whale
from haven.graphql.subscriptions.whale import WhaleUpdateSubscription
from haven.graphql.subscriptions.container import ContainerUpdateSubscription
import docker 
from django.conf import settings
DOWNLOAD_STATUS = "Downloading"
EXTRACTING_STATUS = "Extracting"
PULL_COMPLETE = "Pull complete"
DOWNLOAD_COMPLETE = "Download complete"
PULLED = "Pulled"
WAITING = "Waiting"

class DockerApiConsumer(SyncConsumer):

    def pull_whale(self, message):
        whale_id = message["whale"]
        whale = Whale.objects.get(id=whale_id)

        s = api.api.pull(whale.deployment.image, stream=True, decode=True)

        keeping_progress = []
        finished = []
        


        for f in s:
            if "status" in f:
                if f["status"] in [WAITING]:
                    keeping_progress.append(f["id"])

                if f["status"] in [PULL_COMPLETE]:
                    if f["id"] in keeping_progress:
                        finished.append(f["id"])

                    progress = len(finished) / len(keeping_progress)

                    WhaleUpdateSubscription.broadcast({"whale": whale_id, "pull": { "status" : "Pulling", "progress": progress }}, [WhaleUpdateSubscription.WHALEID_GROUP(whale_id),WhaleUpdateSubscription.USERID_GROUP(whale.creator.id)])
                

        WhaleUpdateSubscription.broadcast({"whale": whale_id, "pull": { "status" : PULLED, "progress": 1 }}, [WhaleUpdateSubscription.WHALEID_GROUP(whale_id),WhaleUpdateSubscription.USERID_GROUP(whale.creator.id)])

        print("Pulled: " + str(message["whale"]))

    def up_whale(self, message):
        whale_id = message["whale"]
        instance = message["instance"]
        network = message["network"]
        command = message["command"]
        whale = Whale.objects.get(id=whale_id)
        print("Whale: " + str(whale_id))

        command = command or whale.deployment.command
        requirements = whale.deployment.requirements

        if "gpu" in requirements:
            device_requests = [
                docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
            ]
        else:
            device_requests = None

        print("Up Whale")
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
                network=network
                or api.networks.list(names=[settings.DOCK["DEFAULT_NETWORK"]])[0].id,
            )
            print("Container Started: " + str(message["whale"]) + "-" + str(message["instance"]))

        WhaleUpdateSubscription.broadcast({"whale": whale_id, "up": { "instance": instance, "container": container.id }}, [WhaleUpdateSubscription.WHALEID_GROUP(whale_id),WhaleUpdateSubscription.USERID_GROUP(whale.creator.id)])
        


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

    