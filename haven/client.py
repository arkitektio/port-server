import docker
import os

api = docker.from_env()


def get_my_networks():
    container_id = os.getenv("HOSTNAME")
    container = api.containers.get(container_id)
    print(container)

    network_settings = container.attrs["NetworkSettings"]
    networks = network_settings["Networks"]
    print("Network Settings:", network_settings)

    expanded_networks = []

    for network_name, network_detail in networks.items():
        network_id = network_detail["NetworkID"]
        network = api.networks.get(network_id)
        expanded_networks.append(network)

    return expanded_networks
