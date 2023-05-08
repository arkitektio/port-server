from balder.types.mutation import BalderMutation
import graphene
from haven import models, types, enums
from haven.client import api
import docker
from django.conf import settings
from lok import bounced
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


class RunWhaleMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)
        instance = graphene.String(required=False)
        command = graphene.String(required=False)
        network = graphene.ID(required=False)

    def mutate(
        self, info, id, instance="main", command=None, network=None
    ):
        whale = models.Whale.objects.get(id=id)
        try:
            api.images.get(whale.deployment.image)
        except docker.errors.ImageNotFound:
            raise Exception("Image not found. Please pull first")


        async_to_sync(channel_layer.send)(
            "docker",
            {
                "type": "up.whale",
                "whale": whale.id,
                "instance": instance,
                "network": network,
                "command": command,
            },
        )

        print("sent up.whale")

        return whale

    class Meta:
        type = types.Whale
        operation = "runWhale"


class CreateWhaleMutation(BalderMutation):
    class Arguments:
        deployment = graphene.ID(required=True)
        client_id = graphene.String(required=True)
        token = graphene.String(required=True)
        fakt_endpoint = graphene.String(required=False)

    @bounced()
    def mutate(
        self,
        info,
        deployment,
        client_id,
        token,
        fakt_endpoint=None,
    ):
        if not fakt_endpoint:
            fakt_endpoint = settings.FAKTS_URL

        whale, x = models.Whale.objects.update_or_create(
            deployment_id=deployment,
            creator=info.context.user,
            defaults=dict(
                token=token,
                url=fakt_endpoint,
                client_id=client_id,
            ),
        )
        return whale

    class Meta:
        type = types.Whale
        operation = "createWhale"


class DeleteWhaleReturn(graphene.ObjectType):
    id = graphene.ID(description="Hallo")


class DeleteWhale(BalderMutation):
    class Arguments:
        id = graphene.ID(description="The ID of the deletable Whale")

    def mutate(root, info, *args, id=None):
        whale = models.Whale.objects.get(id=id)
        whale.delete()
        return {"id": id}

    class Meta:
        type = DeleteWhaleReturn


class PullWhaleReturn(graphene.ObjectType):
    id = graphene.ID(description="Hallo")


class PullWhale(BalderMutation):
    class Arguments:
        id = graphene.ID(description="The ID of the deletabssle Whale")

    def mutate(root, info, *args, id=None):
        whale = models.Whale.objects.get(id=id)
        async_to_sync(channel_layer.send)(
            "docker",
            {
                "type": "pull.whale",
                "whale": whale.id,
            },
        )
        return {"id": id}

    class Meta:
        type = PullWhaleReturn


class PurgeWhale(BalderMutation):
    class Arguments:
        id = graphene.ID(description="The ID of the deletabssle Whale")

    def mutate(root, info, *args, id=None):
        whale = models.Whale.objects.get(id=id)
        api.images.remove(whale.deployment.image)

        return whale

    class Meta:
        type = types.Whale