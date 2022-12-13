from balder.types.query import BalderQuery
import graphene
import docker
from haven import types, models, enums
from haven.client import api
from django.conf import settings
from functools import reduce



class Containers(BalderQuery):
    """Get a single feature by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        status = graphene.List(
            enums.ContainerStatus,
            description="The status to search by (defaults to running)",
            required=False,
        )
        search = graphene.String(
            description="Search for a container by whale", required=False
        )

    def resolve(root, info, status=["running"], search=None):

        filters = {"label": [f"host={settings.DOCK['HOST']}"]}
        if search:
            x = models.Whale.objects.filter(identifier__icontains=search).first()
            if x:
                filters["label"].append(f"whale={x.id}")

        return reduce(
            lambda x, y: x + y,
            [
                api.containers.list(
                    filters={
                        "status": status,
                        **filters,
                    }
                )
                for status in status
            ],
            [],
        )

    class Meta:
        type = types.Container
        list = True
        operation = "containers"


class Container(BalderQuery):
    """Get a single docker by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        id = graphene.ID(description="The Container ID", required=True)

    def resolve(root, info, id):
        t = api.containers.get(id)
        return t

    class Meta:
        type = types.Container
        operation = "container"


class ContainerFor(BalderQuery):
    """Get a single docker by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        whale = graphene.ID(description="The Whale ID", required=True)
        instance = graphene.String(description="The Instance ID", required=False)

    def resolve(root, info, whale, instance="default"):
        t = api.containers.get(f"{whale}-{instance}")
        return t

    class Meta:
        type = types.Container
        operation = "containerFor"
