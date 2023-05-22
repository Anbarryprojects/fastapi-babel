import re
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.base import DispatchFunction
from starlette.types import ASGIApp
from typing import TYPE_CHECKING, Optional
from pathlib import Path

if TYPE_CHECKING:
    from .core import Babel


class InternationalizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        babel: "Babel",
        dispatch: Optional[DispatchFunction] = None,
    ) -> None:
        super().__init__(app, dispatch)
        self.babel: "Babel" = babel

    def get_language(self, lang_code):
        languages = re.findall(r"([a-z]{2}-[A-Z]{2}|[a-z]{2})(;q=\d.\d{1,3})?", lang_code)
        languages = sorted(languages, key=lambda x: x[1], reverse=True)
        for lang in languages: # if language if path and no quantifier
            if lang[0] in [i.name for i in list(Path(self.babel.config.BABEL_TRANSLATION_DIRECTORY).iterdir())] and not len(lang[1]):
                return lang[0]



        for lang in languages:
            if lang[0] in [i.name for i in list(Path(self.babel.config.BABEL_TRANSLATION_DIRECTORY).iterdir())] and len(lang[1]):
                return lang[0]

        return self.babel.config.BABEL_DEFAULT_LOCALE


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
        lang_code: Optional[str] = request.headers.get("Accept-Language", None)
        self.babel.locale = self.get_language(lang_code)

        response: Response = await call_next(request)
        return response
