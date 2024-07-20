import requests
from requests.models import Response
from requests.auth import AuthBase as AuthBase
from collections import Counter


class RequestCounter(Counter):
    max_requests: int = 0

    def incr(self) -> None:
        self["requests"] += 1

    @property
    def cur(self) -> int:
        return self["requests"]

    def set_max(self, count: int) -> None:
        self.max_requests = count


request_counter: RequestCounter = RequestCounter()


def get(
    url: str,
    force_debug: bool = False,
    headers: dict | None = None,
    session: requests.Session | None = None,
) -> Response:
    return request(
        method="get", url=url, headers=headers, force_debug=force_debug, session=session
    )


def request(
    method: str,
    url: str,
    json: dict | None = None,
    headers: dict | None = None,
    force_debug: bool = False,
    session: requests.Session | None = None,
) -> Response:
    if request_counter.max_requests > 0:
        if request_counter.cur > request_counter.max_requests:
            msg = f"max_requests {request_counter.max_requests} reached"
            raise ValueError(msg)
        request_counter.incr()

    mgr = session.request if session else requests.request

    try:
        response = mgr(method=method, url=url, json=json, headers=headers)
        if force_debug:
            debug_request(url, method, response, json, headers)

        return response
    except Exception as ex:
        debug_request(url, method, None, json, headers)
        raise ex


def debug_request(
    url: str,
    method: str,
    response: Response | None = None,
    payload: dict | None = None,
    headers: dict | None = None,
) -> None:
    print("#########################")
    print(f"Debugging request to {url}")
    print(f"Method: {method}")
    print(f"Payload: {payload}")
    print(f"Headers: {headers}")
    if response is not None:
        print(f"Response: {response}")
        print(response.json())
    print("#########################")
