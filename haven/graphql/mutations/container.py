from balder.types.mutation import BalderMutation
import graphene
from haven import models, types, enums
from haven.client import api
import docker
from django.conf import settings


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
            container.stop()
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
            container.restart()
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
            container.remove()
            return container

        else:
            return None

    class Meta:
        type = types.Container
        operation = "removeContainer"
