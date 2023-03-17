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
        network = graphene.ID(required=False)
        runtime = graphene.Argument(enums.DockerRuntime, required=False)

    def mutate(self, info, id, instance="default", network=None, runtime=None):
        whale = models.Whale.objects.get(id=id)

        try:
            container = api.containers.get(f"{whale.id}-{instance}")
            return container
        except docker.errors.NotFound:
            container = api.containers.run(
                whale.image,
                command='arkitekt run port',
                detach=True,
                name=f"{whale.id}-{instance}",
                labels={
                    "whale": f"{whale.id}",
                    "instance": f"{instance}",
                    "host": f"{settings.DOCK['HOST']}",
                },
                restart_policy={"Name": "on-failure", "MaximumRetryCount": 5},
                runtime=runtime or whale.runtime or "runc",
                environment={
                    "FAKTS_URL": whale.url,
                    "FAKTS_TOKEN": whale.token,
                },
                network=network
                or api.networks.list(names=[settings.DOCK["DEFAULT_NETWORK"]])[0].id,
            )
            return container

    class Meta:
        type = types.Container
        operation = "runWhale"




class CreateWhaleMutation(BalderMutation):


    class Arguments:
        version = graphene.String(required=True)
        identifier = graphene.String(required=True)
        image = graphene.String(required=True)
        client_id = graphene.String(required=True)
        token = graphene.String(required=True)
        client_secret = graphene.String(required=True)
        scopes = graphene.List(graphene.String, required=True)
        fakt_endpoint = graphene.String(required=False)
        runtime = graphene.Argument(enums.DockerRuntime, required=False)

    @bounced()
    def mutate(self, info, version, identifier, image, client_id, client_secret, scopes, fakt_endpoint= None, runtime=None, token=None):

        if not fakt_endpoint:
            fakt_endpoint = settings.FAKTS_URL


        whale, x = models.Whale.objects.update_or_create(client_id=client_id, defaults= dict(version=version, identifier=identifier, image=image, runtime=runtime, client_secret=client_secret, scopes=scopes, url=fakt_endpoint, creator=info.context.user, token=token))
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
        id = graphene.ID(description="The ID of the deletable Whale")

    def mutate(root, info, *args, id=None):
        whale = models.Whale.objects.get(id=id)
        async_to_sync(channel_layer.send)("docker", {
            "type": "pull.image",
            "image": whale.image,
        })
        return {"id": id}

    class Meta:
        type = PullWhaleReturn