from balder.types.mutation import BalderMutation
import graphene
from haven import models, types, enums
from haven.client import api
import docker
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()



class StopContainerMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)

    def mutate(
        self,
        info,
        id,
    ):

        container = api.containers.get(id)
        if container:
            async_to_sync(channel_layer.send)("docker", {
            "type": "stop.container",
            "container": id,
            })
            return container

        else:
            return None

    class Meta:
        type = types.Container
        operation = "stopContainer"


class RestartContainerMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):

        container = api.containers.get(id)
        if container:
            async_to_sync(channel_layer.send)("docker", {
            "type": "restart.container",
            "container": id,
            })
            return container

        else:
            return None

    class Meta:
        type = types.Container
        operation = "restartContainer"


class RemoveContainerMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):

        container = api.containers.get(id)
        if container:
            async_to_sync(channel_layer.send)("docker", {
            "type": "remove.container",
            "container": id,
            })
            return container

        else:
            return None

    class Meta:
        type = types.Container
        operation = "removeContainer"
