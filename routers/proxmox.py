from fastapi import APIRouter

from services.proxmox import ProxmoxService


router = APIRouter(
    prefix="/proxmox",
    tags=["Proxmox"],
)

proxmox = ProxmoxService()


@router.get("/nodes")
def get_nodes():
    return proxmox.get_nodes()

@router.get("/nodes/{node}")
def get_node(node: str):
    return proxmox.get_node(node)

@router.get("/nodes/{node}/vms")
def get_vms(node: str):
    return proxmox.get_vms(node)

@router.get("/nodes/{node}/vms/running")
def get_running_vms(node: str):
    return{
	"vms_running": proxmox.get_running_vms()
    }
@router.get("/nodes/{node}/containers")
def get_containers(node: str):
    return proxmox.get_containers(node)

@router.get("/nodes/{node}/containers/running")
def get_running_containers(node: str):
    return{
	"containers_running": proxmox.get_running_containers()
    }

@router.get("/nodes/{node}/network")
def get_network_information(node: str):
    return proxmox.get_network_information(node)

@router.get("/nodes/{node}/network/speed")
def get_network_speed(node: str):
    return proxmox.get_network_speed(node)