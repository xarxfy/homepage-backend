import socket
import time

def check_port(host: str, port: int, timeout: float = 3) -> dict:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            ms = round((time.perf_counter() - start) * 1000, 1)
            return {
                "host": host,
                "port": port,
                "status": "open",
                "ms": ms,
            }
    except ConnectionRefusedError:
        return {
            "host": host,
            "port": port,
            "status": "closed",
            "ms": None,
        }
    except socket.timeout:
            return {
                "host": host,
                "port": port,
                "status": "timeout",
                "ms": None,
            }
    except socket.gaierror:
            return {
                "host": host,
                "port": port,
                "status": "unknown",
                "ms": None,
            }
    except OSError as e:
            return {
                "host": host,
                "port": port,
                "status": "error",
                "ms": None,
                "detail": str(e)
            }