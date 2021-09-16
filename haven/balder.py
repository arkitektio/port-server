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

dockstring = re.compile(r"(?P<namespace>[^\/]*)\/(?P<repo>[^\:]*)\:(?P<tag>[^\s]*)")


class Whale(BalderQuery):
    """ Get information on your Docker Template """


    class Arguments:
        id = graphene.ID(required=True, description="The Template ID")


    @bounced(anonymous=True)
    def resolve(root, info, *args, id=None):
        return models.PortTemplate.objects.get(id=id)


    class Meta:
        type = types.Whale


class Whales(BalderQuery):

    class Meta:
        type = types.Whale
        list = True


class CreateWhaleReturn(graphene.ObjectType):
    whale = graphene.Field(types.Whale)


class CreateWhale(BalderMutation):
    """ Create Port Template (and corresponding ArkitektID)"""

    class Arguments:
        namespace = graphene.String(required=False, description="The Namespace of the Docker (UserName on Dockerhub)")
        repo = graphene.String(required=False, description="The Repo of the Docker (Repo on Dockerhub)")
        branch = graphene.String(required=False, description="The Repo of the Docker (Repo on Dockerhub)")
        user = graphene.String(required=False, description="The User of the Docker (Username on Github)")
        tag = graphene.String(required=False, description="The Tag of the Docker (UserName on Dockerhub)")
        q = graphene.String(required=False, description="The Docker Adress")
        env = GenericScalar(required=False, description="Environment parameters JSON")
        node = graphene.ID(required=False, description="The Node id")


    @bounced(only_jwt=True)
    def mutate(root, info, *args, namespace=None,  repo=None,  branch=None, q=None, user=None, node=None, **kwargs):

        assert user is not None, "Provide User"
        assert repo is not None, "Provide Repo"
        assert branch is not None, "Provide Branch"

        result = requests.get(f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/port.yaml")
        result = requests.get(f"https://raw.githubusercontent.com/jhnnsrs/segmentor/master/port.yaml")
        print(result.content)

        config = yaml.load(result.content)


        assert "image" in config, "The Config didn't provide any image in its configuration. Repo2Docker is currently not supported"
        assert "package" in config, "The Config didn't provide any Package in its configuretaiton. Please get real"
        

       
        # TODO: connect to Arkitekt
        try:
            node = Node.objects.get(package=config["package"], interface=config["interface"])


            temp = Template.objects.create(node=node.id,params={"docker": True})
            print(temp)

        except:
            raise

        model, created = models.PortTemplate.objects.get_or_create(arkitekt_id=temp.id, namespace=namespace, env=env, repo=repo, tag= tag)

        
        return {"whale" : model}


    class Meta:
        type = CreateWhaleReturn


class DeleteWhaleReturn(graphene.ObjectType):
    id = graphene.ID(description="Hallo")

class DeleteWhale(BalderMutation):

    class Arguments:
        id = graphene.ID(description="The ID of the deletable Whale")

    
    def mutate(root, info, *args, id=None):
        whale = models.PortTemplate.objects.get(id=id)
        whale.delete()
        return {"id": id}

    class Meta:
        type = DeleteWhaleReturn