import os
from balder.types import BalderMutation, BalderQuery
from haven import types, models
from haven.filters import GithubRepoFilter
import graphene
from lok import bounced

class GithubRepos(BalderQuery):
    class Meta:
        filter = GithubRepoFilter
        type = types.GithubRepo
        paginate = True
        list = True

class DetailGithubRepo(BalderQuery):
    """Get information on your Docker Template"""

    class Arguments:
        id = graphene.ID(description="The Whale ID", required=True)

    @bounced(anonymous=True)
    def resolve(root, info, *args, id=None, template=None):
        if id:
            return models.GithubRepo.objects.get(id=id)

    class Meta:
        type = types.GithubRepo
        operation = "githubRepo"