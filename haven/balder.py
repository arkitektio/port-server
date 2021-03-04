from django.http import request
from balder.types import BalderMutation, BalderQuery
from haven import types, models
from herre import bounced
import requests
import graphene
from graphene.types.generic import GenericScalar
import re

dockstring = re.compile(r"(?P<namespace>[^\/]*)\/(?P<repo>[^\:]*)\:(?P<tag>[^\s]*)")


class Port(BalderQuery):
    """ Get information on your Docker Template """


    class Arguments:
        id = graphene.ID(required=True, description="The Template ID")


    @bounced(anonymous=True)
    def resolve(root, info, *args, id=None):
        return models.PortTemplate.objects.get(id=id)


    class Meta:
        type = types.PortTemplate


class CreatePort(BalderMutation):
    """ Create Port Template (and corresponding ArkitektID)"""

    class Arguments:
        namespace = graphene.String(required=False, description="The Namespace of the Docker (UserName on Dockerhub)")
        repo = graphene.String(required=False, description="The Repo of the Docker (Repo on Dockerhub)")
        tag = graphene.String(required=False, description="The Tag of the Docker (UserName on Dockerhub)")
        q = graphene.String(required=False, description="The Docker Adress")
        env = GenericScalar(required=False, description="Environment parameters JSON")
        node = graphene.ID(required=True, description="The Node id")


    @bounced(anonymous=True)
    def mutate(root, info, *args, namespace=None,  repo=None,  tag=None, q=None, env=None, node=None):

        if q:
            match = dockstring.match(q)
            if match:
                namespace = match.group("namespace")
                repo = match.group("repo")
                tag = match.group("tag")
            else:
                raise Exception("Don't know how to expand the Q String to Namespace, Repo, Tag, check that it conforms to <hub_user>/<repo_name>:<tag>")

        assert namespace is not None, "Provide Namespace"
        assert repo is not None, "Provide Repo"
        assert tag is not None, "Provide Tag"

        

        # TODO: connect to Arkitekt
        try:
            createTemplateMutation = """
                mutation($node: ID!, $params: GenericScalar) {
                    createTemplate(node: $node, params: $params){
                        id
                    }
                }
            """

            result = requests.post("http://arkitekt:8090/graphql", json={"query": createTemplateMutation, "variables": {
                "node": node,
                "params": {"docker": True}
            }})

            answer = result.json()
            print(answer)

            arkitekt_id = answer["data"]["createTemplate"]["id"]

        except:
            raise Exception("Couldn't create a Template on the associated Arkitekt")

        model, created = models.PortTemplate.objects.get_or_create(arkitekt_id=arkitekt_id, namespace=namespace, env=env, repo=repo, tag= tag)

        
        return model


    class Meta:
        type = types.PortTemplate







