import ipaddress
from fastapi import APIRouter, HTTPException, Query
from services.dns_lookup import lookup, RecordType, DnsLookupError
from services.port_check import check_port
import re

HOSTNAME_RE = re.compile(r"^[a-zA-Z0-9.-]{1,253}$")


router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("/network/dns/lookup")
def dns_lookup(
    name: str = Query(..., min_length=1, max_length=253),
    type: RecordType = RecordType.A,
    server: str | None = None,
):
    if server:
        try:
            ipaddress.ip_address(server)
        except ValueError:
            raise HTTPException(400, "Server muss eine IP-Adresse sein")

    try:
        return lookup(name.strip(), type, server)
    except DnsLookupError as e:
        raise HTTPException(e.status_code, e.message)
    
@router.get("/network/portcheck")
def port_check(
    host: str = Query(..., min_length=1, max_length=253),
    port: int = Query(..., ge=1, le=65535)
):
    host = host.strip()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not HOSTNAME_RE.match(host):
            raise HTTPException(400, "Invalid IP Address")
    return check_port(host, port)