from balder.types import BalderSubscription
from lok import bounced
import graphene
from haven import models, types
import logging

logger = logging.getLogger(__name__)






class ContainerEvent(graphene.ObjectType):
    up =  graphene.Field(types.UpEvent)


class ContainerUpdateSubscription(BalderSubscription):
    CONTAINER_GROUP = lambda container: f"container_{container.id}"

    class Arguments:
        id = graphene.ID()

    class Meta:
        type = ContainerEvent

    def publish(payload, info, *args, **kwargs):
        payload = payload["payload"]


        logger.error("error in payload")

    @bounced(only_jwt=True)
    def subscribe(root, info,id, *args, **kwargs):
        return [ContainerUpdateSubscription.CONTAINER_GROUP(id)]


