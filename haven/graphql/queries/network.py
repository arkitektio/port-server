from balder.types.query import BalderQuery
import graphene
import docker
from haven import types, models
from haven.client import api


class Networks(BalderQuery):
    """Get a single feature by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        id = graphene.ID(description="The ID to search by", required=False)

    def resolve(root, info, id=None):

        networks = api.networks.list()

        return networks

    class Meta:
        type = types.Network
        list = True
        operation = "networks"
