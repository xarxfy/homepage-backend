import os

from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI
from enum import Enum
load_dotenv()

class VMAction(str, Enum):
    start = "start"
    shutdown = "shutdown"
    stop = "stop"
    reboot = "reboot"

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

    #VM Methods
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

    def vm_actions(self, node: str, vmid: int, action: VMAction):
            status = self.proxmox.nodes(node).qemu(vmid).status
            return getattr(status, action.value).post()

    #Container Methods
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
    
    def container_actions(self, node: str, vmid: int, action: VMAction):
                status = self.proxmox.nodes(node).lxc(vmid).status
                return getattr(status, action.value).post()

    #Network Methods
    def get_network_information(self, node: str):
        return self.proxmox.nodes(node).network.get()

    def get_dns_information(self, node: str):
        return self.proxmox.nodes(node).dns.get()
    
    #Authentication Methods
    def get_users_information(self):
        return self.proxmox.access.users.get()
    
    def get_api_tokens(self):
        tokens = []
        for user in self.proxmox.access.users.get():
            userid = user["userid"]
            for t in self.proxmox.access.users(userid).token.get():
                details = self.proxmox.access.users(userid).token(t["tokenid"]).get()
                tokens.append({"userid": userid, "tokenid": t["tokenid"], **details})
        return tokens
    
    def delete_api_token(self, userid: str, tokenid: str):
        self.proxmox.access.users(userid).token(tokenid).delete()
        
    def create_api_token(self, userid: str, tokenid: str, comment: str, privsep: int):
        return self.proxmox.access.users(userid).token(tokenid).post(
            comment=comment,
            privsep=privsep,
        )