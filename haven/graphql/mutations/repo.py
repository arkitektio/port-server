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
from haven.utils import download_logo


class ScanRepoReturn(graphene.ObjectType):
    status = graphene.String()
    message = graphene.String()
    repo = graphene.Field(types.GithubRepo)
    deployments = graphene.List(types.Deployment)


def scan_repo(repo: models.GithubRepo):
    # download the pryproject toml file
    x = requests.get(repo.deployments_url, headers={"Cache-Control": "no-cache"})
    # parse the file
    z = yaml.safe_load(x.text)
    print(z)

    deps = []
    try:
        for deployment_dict in z["deployments"]:
            manifest_dict = deployment_dict["manifest"]

            manifest, _ = models.Manifest.objects.update_or_create(
                version=manifest_dict["version"],
                identifier=manifest_dict["identifier"],
                defaults=dict(
                    logo=manifest_dict.get("logo", None),
                    scopes=manifest_dict["scopes"],
                    requirements=manifest_dict["requirements"],
                    entrypoint=manifest_dict["entrypoint"],
                ),
            )

            logo = manifest_dict.get("logo", None)
            if logo:
                manifest.logo.save(f"logo{manifest.id}.png", download_logo(logo))
                manifest.save()

            dep, _ = models.Deployment.objects.update_or_create(
                deployment_id=deployment_dict["deployment_id"],
                defaults=dict(
                    repo=repo,
                    manifest=manifest,
                    builder=deployment_dict["builder"],
                    image=deployment_dict["image"],
                    definitions=deployment_dict["definitions"],
                    deployed_at=deployment_dict["deployed_at"],
                    build_id=deployment_dict["build_id"],
                ),
            )

            deps.append(dep)
    except KeyError as e:
        pass

    return deps


class ScanRepoMutation(BalderMutation):
    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id, instance="default", network=None, runtime=None):
        repo = models.GithubRepo.objects.get(id=id)

        # download the pryproject toml file
        x = requests.get(repo.deployments_url, headers={"Cache-Control": "no-cache"})
        # parse the file
        z = yaml.safe_load(x.text)
        print(z)

        deps = []
        try:
            for deployment_dict in z["deployments"]:
                manifest_dict = deployment_dict["manifest"]

                manifest, _ = models.Manifest.objects.update_or_create(
                    version=manifest_dict["version"],
                    identifier=manifest_dict["identifier"],
                    defaults=dict(
                        logo=manifest_dict.get("logo", None),
                        scopes=manifest_dict["scopes"],
                        requirements=manifest_dict["requirements"],
                        entrypoint=manifest_dict["entrypoint"],
                    ),
                )

                logo = manifest_dict.get("logo", None)
                if logo:
                    manifest.logo.save(f"logo{manifest.id}.png", download_logo(logo))
                    manifest.save()

                dep, _ = models.Deployment.objects.update_or_create(
                    deployment_id=deployment_dict["deployment_id"],
                    defaults=dict(
                        repo=repo,
                        manifest=manifest,
                        builder=deployment_dict["builder"],
                        image=deployment_dict["image"],
                        definitions=deployment_dict["definitions"],
                        deployed_at=deployment_dict["deployed_at"],
                        build_id=deployment_dict["build_id"],
                    ),
                )

                deps.append(dep)
        except KeyError as e:
            pass
            return ScanRepoReturn(
                status="error", message=str(e), repo=repo, deployments=[]
            )

        return ScanRepoReturn(
            status="success", message="Scanned Repo", repo=repo, deployments=deps
        )

    class Meta:
        list = True
        type = ScanRepoReturn
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

        model, _ = models.GithubRepo.objects.get_or_create(
            user=user,
            repo=repo,
            branch=branch,
        )

        deps = scan_repo(model)

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
