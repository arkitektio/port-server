import os
from django.http import request
from balder.types import BalderMutation, BalderQuery
from haven import types, models
from lok import bounced
import requests
import graphene
from graphene.types.generic import GenericScalar
import re
from arkitekt.schema import Node, Template
import requests
import yaml
from django.conf import settings


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

dockstring = re.compile(r"(?P<namespace>[^\/]*)\/(?P<repo>[^\:]*)\:(?P<tag>[^\s]*)")


class DetailWhale(BalderQuery):
    """Get information on your Docker Template"""

    class Arguments:
        id = graphene.ID(description="The Whale ID")
        template = graphene.ID(description="The Template ID")

    @bounced(anonymous=True)
    def resolve(root, info, *args, id=None, template=None):
        if id:
            return models.Whale.objects.get(id=id)
        if template:
            return models.Whale.objects.get(template=template)

    class Meta:
        type = types.Whale
        operation = "whale"


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


class Whales(BalderQuery):
    class Meta:
        type = types.Whale
        list = True


class CreateWhaleReturn(graphene.ObjectType):
    whale = graphene.Field(types.Whale)


class GithubRepos(BalderQuery):
    class Meta:
        type = types.GithubRepo
        list = True


class CreateGithubRepo(BalderMutation):
    class Arguments:
        repo = graphene.String(
            required=True, description="The Repo of the Docker (Repo on Dockerhub)"
        )
        branch = graphene.String(
            required=True, description="The Repo of the Docker (Repo on Dockerhub)"
        )
        user = graphene.String(
            required=True, description="The User of the Docker (Username on Github)"
        )

    @bounced()
    def mutate(root, info, user=None, repo=None, branch=None):

        assert user is not None, "Provide User"
        assert repo is not None, "Provide Repo"
        assert branch is not None, "Provide Branch"

        result = requests.get(
            f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/.port/definition.yaml"
        )
        result = requests.get(
            f"https://raw.githubusercontent.com/jhnnsrs/om/master/.port/definition.yaml"
        )

        definition = yaml.load(result.content, Loader=Loader)

        model = models.GithubRepo.objects.create(
            user=user,
            repo=repo,
            scopes=["introspection"],
            definition=definition,
            backend=False,
            image="jhnnsrs/ome:latest",
        )

        return model

    class Meta:
        type = types.GithubRepo


class CreateWhale(BalderMutation):
    """Create Port Template (and corresponding ArkitektID)"""

    class Arguments:
        repo = graphene.ID(
            required=False, description="The Repo of the Docker (Repo on Dockerhub)"
        )
        config = GenericScalar(description="The Konfiguration we want to use")

    @bounced()
    def mutate(
        root,
        info,
        repo=None,
        config=None,
        **kwargs,
    ):

        assert repo is not None, "Provide Repo"

        with open(os.path.join(settings.BASE_DIR, "fakts.yaml"), "r") as stream:
            config = yaml.load(stream, Loader=Loader)

        repo = models.GithubRepo.objects.get(id=repo)

        assert (
            repo.image is not None
        ), "Repository must have a Image (please cause a build before)"

        # TODO: connect to Arkitekt
        try:
            node = Node.objects.create(**repo.definition)

            temp = Template.objects.create(
                node=node.id, params={"docker": True}, extensions=["whale"]
            )
            print(temp)

        except:
            raise

        model, created = models.Whale.objects.update_or_create(
            template=temp.id, defaults={"image": repo.image, "config": config}
        )
        repo.whale = model
        repo.save()

        return model

    class Meta:
        type = types.Whale


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


class DeleteGithubRepoReturn(graphene.ObjectType):
    id = graphene.ID(description="Hallo")


class DeleteGithubRepo(BalderMutation):
    class Arguments:
        id = graphene.ID(description="The ID of the deletable Whale")

    def mutate(root, info, *args, id=None):
        repo = models.GithubRepo.objects.get(id=id)
        repo.delete()
        return {"id": id}

    class Meta:
        type = DeleteGithubRepoReturn
