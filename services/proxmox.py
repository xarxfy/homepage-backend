import os

from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI


load_dotenv()

class ProxmoxService:
    def __init__(self):
        self.proxmox = ProxmoxAPI(
            os.getenv("PROXMOX_HOST"),
            user=os.getenv("PROXMOX_USER"),
            token_name=os.getenv("PROXMOX_TOKEN_ID"),
            token_value=os.getenv("PROXMOX_TOKEN_SECRET"),
            verify_ssl=False,
        )

    def get_nodes(self):
        return self.proxmox.nodes.get()

    def get_node(self, node: str):
        return self.proxmox.nodes(node).status.get()

    def get_vms(self, node: str):
        return self.proxmox.nodes(node).qemu.get()

    def get_running_vms(self):
        running_vms = 0

        for node in self.get_nodes():
            vms = self.get_vms(node["node"])

            for vm in vms:
                if vm["status"] == "running":
                    running_vms += 1

        return running_vms

    def get_containers(self, node: str):
        return self.proxmox.nodes(node).lxc.get()

    def get_running_containers(self):
        running_containers = 0

        for node in self.get_nodes():
            containers = self.get_containers(node["node"])

            for container in containers:
                if container["status"] == "running":
                    running_containers += 1

        return running_containers

    def get_network_information(self, node: str):
        return self.proxmox.nodes(node).network.get()