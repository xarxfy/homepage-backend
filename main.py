from fastapi import FastAPI, APIRouter

from routers.proxmox import router as proxmox_router
from routers.tools import router as tools_router

app = FastAPI()

api_router = APIRouter(
	prefix="/api/v1"
)

@api_router.get("/health")
def health():
	return{"status": "ok"}

api_router.include_router(proxmox_router)
api_router.include_router(tools_router)
app.include_router(api_router)
