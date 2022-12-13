import os
from balder.types import BalderMutation, BalderQuery
from haven import types, models, filters
import graphene
from lok import bounced




class Whales(BalderQuery):
    class Meta:
        type = types.Whale
        filter = filters.WhaleFilter
        list = True



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