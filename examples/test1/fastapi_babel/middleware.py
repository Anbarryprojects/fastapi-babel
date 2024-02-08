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

LANGUAGES_PATTERN = re.compile(r"([a-z]{2})-?([A-Z]{2})?(;q=\d.\d{1,3})?")

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
        """Applies an available language.

            To apply an available language it will be searched in the language folder for an available one
            and also it will priotize the one with the highest quality value. The Fallback language will be the
            taken from the BABEL_DEFAULT_LOCALE var.

                Args:
                    lang_code (str): The Value of the Accept-Language Header.

                Returns:
                    str: The language that should be used.
                """
        if not lang_code:
            return self.babel.config.BABEL_DEFAULT_LOCALE

        matches = re.finditer(LANGUAGES_PATTERN, lang_code)
        languages = [(f"{m.group(1)}{ f'_{m.group(2)}' if m.group(2) else ''}", m.group(3) or "") for m in matches]
        languages = sorted(languages, key=lambda x: x[1], reverse=True) # sort the priority, no priority comes last
        translation_directory = Path(self.babel.config.BABEL_TRANSLATION_DIRECTORY)
        translation_files = [i.name for i in translation_directory.iterdir()]
        explicit_priority = None

        for lang, quality in languages:
            if lang in translation_files:
                if not quality:  # languages without quality value having the highest priority 1
                    return lang

                elif not explicit_priority:  # set language with explicit priority <= priority 1
                    explicit_priority = lang

        # Return language with explicit priority or default value
        return explicit_priority if explicit_priority else self.babel.config.BABEL_DEFAULT_LOCALE

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
