import httpx

_request_client = None


def get_request_client() -> httpx.AsyncClient:
    global _request_client
    if _request_client is None:
        _request_client = httpx.AsyncClient(timeout=None)
    return _request_client
