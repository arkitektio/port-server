from balder.types.mutation import BalderMutation
import graphene
from haven import models, types, enums
from haven.client import api
import docker
from django.conf import settings
import requests
import toml
from lok import bounced
import yaml


class ScanRepoMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id, instance="default", network=None, runtime=None):
        repo = models.GithubRepo.objects.get(id=id)

        # download the pryproject toml file
        x = requests.get(repo.deployments_url)
        # parse the file
        z = yaml.safe_load(x.text)
        print(z)

        deps = []

        for deployment in z["deployments"]:
            s, _ = models.Deployment.objects.update_or_create(
                version=deployment["version"],
                identifier=deployment["identifier"],
                defaults=dict(
                    repo=repo,
                    command=deployment["command"],
                    entrypoint=deployment["entrypoint"],
                    image=deployment["image"],
                    requirements=deployment["requirements"],
                    scopes=deployment["scopes"],
                ),
            )
            deps.append(s)

        # TODO: FIX this once on a proper computer
        return deps[0]

    class Meta:
        list = True
        type = types.Deployment
        operation = "scanRepo"


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

        model = models.GithubRepo.objects.create(
            user=user,
            repo=repo,
            branch=branch,
        )

        return model

    class Meta:
        type = types.GithubRepo


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
