import dns.resolver
import dns.reversename
import dns.exception
from enum import Enum

class RecordType(str, Enum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    NS = "NS"
    PTR = "PTR"
    
class DnsLookupError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        
def lookup(name: str, rtype: RecordType, server: str | None = None) -> dict:
    resolver = dns.resolver.Resolver()
    resolver.lifetime = 3
    if server:
        resolver.nameservers = [server]
    query = dns.reversename.from_address(name) if rtype == RecordType.PTR else name
    
    try:
        answer = resolver.resolve(query, rtype.value)
    except dns.resolver.NXDOMAIN:
        raise DnsLookupError(404, f"{name} existiert nicht")
    except dns.resolver.NoAnswer:
        return {"name": name, "type": rtype.value, "server": resolver.nameservers[0], "ttl": None, "records": []}
    except dns.exception.Timeout:
        raise DnsLookupError(504, "DNS-Server antwortet nicht")
    except (dns.exception.DNSException, ValueError) as e:
        raise DnsLookupError(400, str(e))
    
    return {
        "name": name,
        "type": rtype.value,
        "server": resolver.nameservers[0],
        "ttl": answer.rrset.ttl,
        "records": [r.to_text() for r in answer],
    }