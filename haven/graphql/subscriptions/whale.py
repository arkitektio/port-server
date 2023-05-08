from balder.types import BalderSubscription
from lok import bounced
import graphene
from haven import models, types
import logging

logger = logging.getLogger(__name__)







class WhaleUpdateSubscription(BalderSubscription):
    WHALEID_GROUP = lambda whale: f"whale_{id}"
    USERID_GROUP = lambda user: f"whales_user_{id}"

    class Arguments:
        id = graphene.ID(required=False)

    class Meta:
        type = types.WhaleEvent
        operation = "whalesEvent"

    def publish(payload, info, *args, **kwargs):
        return payload["payload"]

    @bounced(only_jwt=True)
    def subscribe(root, info, *args, id = None, **kwargs):
        print("SUBSCRIBING")
        if id is not None:
            return [WhaleUpdateSubscription.WHALEID_GROUP(id)]
        else:
            return [WhaleUpdateSubscription.USERID_GROUP(info.context.user.id)]

