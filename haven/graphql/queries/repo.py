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
        id = graphene.ID(description="The Whale ID", required=False)
        tag = graphene.String(
            description="The tag of the repository e.g jhnnsrs/port:main",
            required=False,
        )

    @bounced(anonymous=True)
    def resolve(root, info, *args, id=None, tag=None):
        if id:
            return models.GithubRepo.objects.get(id=id)
        if tag:
            try:
                user, rest = tag.split("/")
                repo, branch = rest.split(":")
            except ValueError:
                raise ValueError("Invalid Tag format (branch/user:repo)")
            return models.GithubRepo.objects.get(user=user, repo=repo, branch=branch)

    class Meta:
        type = types.GithubRepo
        operation = "githubRepo"
