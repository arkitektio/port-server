from balder.types.query import BalderQuery
import graphene
import docker
from haven import types, models
from haven.client import api
import os


class Networks(BalderQuery):
    """Get a single feature by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        name = graphene.String(description="The ID to search by", required=False)
        limit = graphene.Int(description="The limit of the query", required=False)
        values = graphene.List(
            graphene.ID, description="The IDs to search by", required=False
        )

    def resolve(root, info, limit=20, values=None, id=None):
        networks = api.networks.list()

        if values:
            networks = [n for n in networks if n.id in values]

        return networks[:limit]

    class Meta:
        type = types.Network
        list = True
        operation = "networks"


class MyNetwork(BalderQuery):
    class Arguments:
        pass

    def resolve(root, info):
        return expanded_networks

    class Meta:
        type = types.Network
        list = True
        operation = "mynetworks"
