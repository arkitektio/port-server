from channels.consumer import SyncConsumer
from haven.client import api

class DockerApiConsumer(SyncConsumer):

    def pull_image(self, message):
        s = api.api.pull(message["image"], stream=True, decode=True)
        for f in s:
            print(f)

        print("Pulled: " + message["image"])


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

    