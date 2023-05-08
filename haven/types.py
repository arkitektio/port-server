from balder.types import BalderObject
from haven import models
import graphene
from graphene.types.generic import GenericScalar
from haven.client import api
from haven.enums import DockerRuntime, ContainerStatus, PullProgressStatus, UpProgressStatus
import datetime


class PullEvent(graphene.ObjectType):
    progress = graphene.Float()
    status = graphene.Field(PullProgressStatus)


class UpEvent(graphene.ObjectType):
    container = graphene.ID()


class WhaleEvent(graphene.ObjectType):
    pull =  graphene.Field(PullEvent)
    up = graphene.Field(UpEvent)
    whale = graphene.ID()



class GithubRepo(BalderObject):
    readme = graphene.String()

    def resolve_readme(self, info):
        return self.readme_url

    class Meta:
        model = models.GithubRepo


class Deployment(BalderObject):
    version = graphene.String(required=True)
    identifier = graphene.String(required=True)
    scopes = graphene.List(graphene.String, required=True)
    logo = graphene.String(required=False)

    def resolve_logo(self, info):
        return self.logo.url if self.logo else None


    class Meta:
        model = models.Deployment


class Whale(BalderObject):
    pulled = graphene.Boolean()
    latest_pull = graphene.DateTime()
    containers = graphene.List(lambda: Container)
    latest_event = graphene.Field(WhaleEvent)

    def resolve_containers(self, info):
        return api.containers.list(filters={"label": [f"whale={self.id}"]})

    def resolve_pulled(self, info):
        try:
            api.images.get(self.deployment.image)
            return True
        except:
            return False

    def resolve_latest_pull(self, info):
        try:
            l = api.images.get(self.deployment.image).attrs["Created"]
            l = l.replace("'", "")
            l = l[:24]
            print(l)

        except:
            return None
        format = "%Y-%m-%dT%H:%M:%S.%f"
        return datetime.datetime.strptime(l, format)

    class Meta:
        model = models.Whale


class Network(graphene.ObjectType):
    name = graphene.String()
    id = graphene.String(required=True)
    driver = graphene.String()
    scope = graphene.String()
    ipam = GenericScalar()
    internal = graphene.Boolean()
    containers = graphene.List(lambda: Container)
    options = GenericScalar()
    labels = GenericScalar()


class Image(graphene.ObjectType):
    id = graphene.String(required=True)
    attrs = GenericScalar()
    labels = GenericScalar()
    tags = graphene.List(graphene.String)


class Container(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    image = graphene.Field(Image)
    labels = GenericScalar()
    attrs = GenericScalar()
    whale = graphene.Field(Whale)
    status = graphene.Field(ContainerStatus)
    logs = graphene.String(
        stdout=graphene.Boolean(required=False),
        stderr=graphene.Boolean(required=False),
        tail=graphene.Int(required=False),
        since=graphene.String(required=False),
        timestamps=graphene.Boolean(required=False),
        follow=graphene.Boolean(required=False),
        until=graphene.String(required=False),
    )
    network = graphene.Field(Network)
    runtime = graphene.Field(DockerRuntime)

    def resolve_id(self, info):
        return self.id

    def resolve_labels(self, info):
        return self.labels

    def resolve_whale(self, info):
        whale_label = self.labels.get("whale")
        if whale_label:
            try:
                return models.Whale.objects.get(id=whale_label)
            except models.Whale.DoesNotExist:
                return None

    def resolve_network(self, info):
        id = list(self.attrs["NetworkSettings"]["Networks"].values())[0]["NetworkID"]
        if id:
            return api.networks.get(id)
        else:
            return None

    def resolve_runtime(self, info):
        return self.attrs["HostConfig"]["Runtime"]

    def resolve_attrs(self, info):
        return self.attrs

    def resolve_logs(
        self,
        info,
        stdout=True,
        stderr=True,
        tail=100,
        since=None,
        timestamps=False,
        follow=False,
        until=None,
    ):
        assert info.context.user.is_authenticated, "You must be logged in to see this"
        return self.logs(
            stdout=stdout,
            stderr=stderr,
            tail=tail,
            since=since,
            timestamps=timestamps,
            follow=follow,
            until=until,
        ).decode("utf-8")
