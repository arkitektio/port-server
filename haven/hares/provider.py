from delt.messages.provision import ProvisionMessage
import aiormq
from haven.models import PortPod, PortTemplate
from asgiref.sync import sync_to_async
import aiodocker
import logging
from delt.bridge import arkitekt


logger = logging.getLogger(__name__)


createPodMutation = """
    mutation($template: ID!){
        createPod(template: $template){
            id
            name
        }

    }
"""



@sync_to_async
def get_template_from_provision(provision: ProvisionMessage)-> PortTemplate:

    template = PortTemplate.objects.get(arkitekt_id=provision.data.template)
    return template


@sync_to_async
def create_pod_from_provision(provision: ProvisionMessage, template: PortTemplate) -> PortPod:
    
    answer = arkitekt.call(createPodMutation, {"template": provision.data.template })

    arkitekt_id = answer["createPod"]["id"]
    arkitekt_name = answer["createPod"]["name"]

    pod, created = PortPod.objects.get_or_create(
            arkitekt_id = arkitekt_id,
            defaults= {
                "template": template,
                "name": arkitekt_name
            }
    )

    return pod


class PortProviderRabbit:
    provider_name = "port"

    def __init__(self, *args, **kwargs) -> None:
        assert self.provider_name is not None, f"Please overwrite provider_name attr in {self.__class__.__name__}"
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.connection = await aiormq.connect(f"amqp://guest:guest@mister/")
        self.channel = await self.connection.channel()
        self.docker = aiodocker.Docker()

        # This queue gets called from the HTTP backend (so GraphQL Postman request) with an already created Assignation
        self.provision_in = await self.channel.queue_declare(f"{self.provider_name}_provision_in")

        # Start listening the queue with name 'hello'
        await self.channel.basic_consume(self.provision_in.queue, self.on_provision_in)


    @ProvisionMessage.unwrapped_message
    async def on_provision_in(self, provision: ProvisionMessage, message: aiormq.types.DeliveredMessage):
        
        template = await get_template_from_provision(provision)
        pod = await create_pod_from_provision(provision, template)

        logger.info('== Running a hello-world container ==')
        
        try:
            container = await self.docker.containers.create_or_replace(
                config={
                    'Image': "hello-world", ##f"{template.namespace}/{template.repo}:{template.tag}",
                    'Network': "container:arbeider",
                    "Env": [
                        f"ARKITEKT_POD_ID={pod.arkitekt_id}",
                        f"ARKITEKT_HOST=p-tnagerl-lab1"
                    ]
                },
                name=pod.name,
            )


            started = await container.start()
            logs = await container.log(stdout=True)
            print(''.join(logs))

            provision.data.pod = pod.id

            await self.channel.basic_publish(
                provision.to_message(), routing_key="provision_done",
                properties=aiormq.spec.Basic.Properties(
                    correlation_id=provision.meta.reference
                )
            )
    
        except Exception as e:
            logger.error(e)


        await message.channel.basic_ack(message.delivery.delivery_tag)