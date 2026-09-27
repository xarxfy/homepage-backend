from fastapi import APIRouter

from services.proxmox import ProxmoxService, VMAction


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

#VM Methods
@router.get("/nodes/{node}/vms")
def get_vms(node: str):
    return proxmox.get_vms(node)

@router.get("/nodes/{node}/vms/running")
def get_running_vms(node: str):
    return{
	"vms_running": proxmox.get_running_vms()
    }
    
@router.post("/nodes/{node}/vms/{vmid}/{action}")
def vm_action(node: str, vmid: int, action: VMAction):
    upid = proxmox.vm_actions(node, vmid, action)
    return {"vmid": vmid, "action": action.value, "tast": upid}


#Container Methods    
@router.get("/nodes/{node}/containers")
def get_containers(node: str):
    return proxmox.get_containers(node)

@router.get("/nodes/{node}/containers/running")
def get_running_containers(node: str):
    return{
	"containers_running": proxmox.get_running_containers()
    }
    
@router.post("/nodes/{node}/containers/{vmid}/{action}")
def container_action(node: str, vmid: int, action: VMAction):
    upid = proxmox.container_actions(node, vmid, action)
    return {"vmid": vmid, "action": action.value, "tast": upid}
    
#Network Methods
@router.get("/nodes/{node}/network")
def get_network_information(node: str):
    return proxmox.get_network_information(node)

@router.get("/nodes/{node}/network/dns")
def get_dns_information(node: str):
    return proxmox.get_dns_information(node)
