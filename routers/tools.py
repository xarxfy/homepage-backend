import ipaddress
from fastapi import APIRouter, HTTPException, Query
from services.dns_lookup import lookup, RecordType, DnsLookupError

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