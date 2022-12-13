from balder.types.query import BalderQuery
import graphene
import docker
from haven import types, models, enums
from haven.client import api
from django.conf import settings
from functools import reduce


class RepoScans(BalderQuery):
    """Get a single feature by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Meta:
        type = types.RepoScan
        list = True
        operation = "reposcans"


class Scan(BalderQuery):
    """Get a single docker by ID

    Returns a single feature by ID. If the user does not have access
    to the feature, an error will be raised.
    """

    class Arguments:
        id = graphene.ID(description="The Container ID", required=True)

    def resolve(root, info, id):
        return models.RepoScan.objects.get(id=id)

    class Meta:
        type = types.RepoScan
        operation = "reposcan"
