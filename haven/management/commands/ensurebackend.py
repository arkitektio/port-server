from django.core.management.base import BaseCommand
from django.conf import settings
import docker



import logging
import sys



logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Checks if docker api is okay"

    def handle(self, *args, **kwargs):

        try:
            api = docker.from_env()
        except Exception as e:
            logger.critical("Cannot connect to docker api. Did you mount the docker socket?", exc_info=True)
            sys.exit(1)

        try:
            containers = api.containers.list()
        except Exception as e:
            logger.critical("Cannot list containers, docker api might be broken. Did you mount the docker socket?", exc_info=True)
            sys.exit(1)

        try:
            api.networks.list(names=[settings.DOCK["DEFAULT_NETWORK"]])[0].id
        except Exception as e:
            logger.critical(f"Default {settings.DOCK['DEFAULT_NETWORK']} Network is not available. Please speficy it correctly in the config", exc_info=True)
            sys.exit(1)

        
