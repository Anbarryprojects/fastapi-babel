from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.base import DispatchFunction
from starlette.types import ASGIApp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Babel


class InternationalizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, babel: "Babel", dispatch: DispatchFunction = None
    ) -> None:
        super().__init__(app, dispatch)
        self.babel: "Babel" = babel

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        lang_code: str = request.headers.get("Accept-Language", None)
        if lang_code:
            self.babel.locale = lang_code
        response = await call_next(request)
        return response
