import copy
import time
import uuid
from http import HTTPStatus
from typing import TYPE_CHECKING

from starlette.datastructures import URL, MutableHeaders

from ..config import constants
from ..entrypoints import get_logger

if TYPE_CHECKING:
    from typing import TypeAlias

    from starlette.types import ASGIApp, Message, Receive, Scope, Send

    THasHeaders: TypeAlias = "Scope" | "Message"


def _copy_headers(asgi: "THasHeaders"):
    headers = copy.deepcopy(asgi["headers"])
    return {key.decode("latin1"): value.decode("latin1") for key, value in headers}


def _extract_req_info(scope: "Scope"):
    url = URL(scope=scope)
    return {
        "http": f"{scope['scheme'].upper()}/{scope['http_version']}",
        "method": scope["method"],
        "path": url.path,
        "query": url.query,
        "headers": _copy_headers(scope),
        "client": "{!s}:{!s}".format(*scope["client"]) if scope["client"] else "-:-",
    }


def _extract_res_info(message: "Message"):
    return {
        "status_code": message["status"],
        "phrase": HTTPStatus(message["status"]).phrase,
        "headers": _copy_headers(message),
    }


class MessageLoggerMiddleware:
    def __init__(self, app: "ASGIApp") -> None:
        self.app = app
        logger = None
        if hasattr(self.app, "state"):
            logger = getattr(app.state, "logger", None)  # type: ignore
        if not logger:
            logger = get_logger()
        self.logger = logger

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        async def logger_send(message: "Message"):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=message["headers"])
                headers.append(
                    constants.RES_TIME_ELAPSE, f"{time.perf_counter() - start_response:.3f}s"
                )
                extra_info["response"] = _extract_res_info(message)
            await send(message)

        extra_info = {}
        if scope["type"] not in {"http", "https"}:
            return await self.app(scope, receive, send)

        extra_info["request"] = _extract_req_info(scope)
        start_response = time.perf_counter()
        headers = MutableHeaders(scope=scope)
        headers.update({constants.REQ_ID_HEADER: str(uuid.uuid4())})
        try:
            await self.app(scope, receive, logger_send)
        finally:
            # Here is where the log message goes
            self.logger.info("Trace access ASGI connection", extra=extra_info)
