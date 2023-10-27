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


        
