from balder.types.mutation import BalderMutation
import graphene
from haven import models, types, enums
from haven.client import api
import docker
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class DeleteDeploymentReturn(graphene.ObjectType):
    id = graphene.ID(description="Hallo")


class DeleteDeployment(BalderMutation):
    class Arguments:
        id = graphene.ID(description="The ID of the deletable Whale")

    def mutate(root, info, *args, id=None):
        repo = models.Deployment.objects.get(id=id)
        repo.delete()
        return {"id": id}

    class Meta:
        type = DeleteDeploymentReturn
