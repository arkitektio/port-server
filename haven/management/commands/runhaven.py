from pydantic import BaseModel
from django.core.management import BaseCommand
from haven.hares.provider import PortProviderRabbit
import asyncio


async def main(rabbit):
    # Perform connection
    await rabbit.connect()



class Command(BaseCommand):

    leave_locale_alone = True

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)


    def handle(self, *args, **options):

        rabbit = PortProviderRabbit()
        # Get the backend to use
        
        loop = asyncio.get_event_loop()
        loop.create_task(main(rabbit))

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        print(" [x] Awaiting Provision requests")
        loop.run_forever()