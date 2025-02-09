import re
from pathlib import Path
from typing import Optional, Callable
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint

from .core import Babel, _context_var
from .properties import RootConfigs

LANGUAGES_PATTERN = re.compile(r"([a-z]{2})-?([A-Z]{2})?(;q=\d.\d{1,3})?")

class BabelMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        babel_configs: RootConfigs,
        jinja2_templates: Optional[Jinja2Templates] = None,
        dispatch: Optional[DispatchFunction] = None,
        locale_selector: Optional[Callable[[Request], Optional[str]]] = None,
    ) -> None:
        """
        :param locale_selector: a callable that takes the request and returns
                                a locale string (e.g. 'de' or 'en'), or None if
                                no override is desired.
        """
        super().__init__(app, dispatch)
        self.babel_configs = babel_configs
        self.jinja2_templates = jinja2_templates
        self.locale_selector = locale_selector

    def get_language(self, babel: Babel, lang_code: str) -> str:
        """Original Babel logic that parses Accept-Language."""
        if not lang_code:
            return babel.config.BABEL_DEFAULT_LOCALE

        matches = re.finditer(LANGUAGES_PATTERN, lang_code)
        languages = [
            (f"{m.group(1)}{f'_{m.group(2)}' if m.group(2) else ''}", m.group(3) or "")
            for m in matches
        ]
        languages = sorted(
            languages, key=lambda x: x[1], reverse=True
        )  # priority sort
        translation_directory = Path(babel.config.BABEL_TRANSLATION_DIRECTORY)
        translation_files = [i.name for i in translation_directory.iterdir()]
        explicit_priority = None

        for lang, quality in languages:
            if lang in translation_files:
                # no quality => highest priority
                if not quality:
                    return lang
                # remember the first we see with explicit priority
                elif not explicit_priority:
                    explicit_priority = lang

        # fallback: either the explicit_priority or default locale
        return explicit_priority or self.babel_configs.BABEL_DEFAULT_LOCALE

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        lang_code: Optional[str] = request.headers.get("Accept-Language", None)

        # Create a new Babel instance per request
        request.state.babel = Babel(configs=self.babel_configs)

        # 1) If a custom locale_selector is provided, call it first
        override_locale = None
        if self.locale_selector:
            override_locale = self.locale_selector(request)

        # 2) If no override, fallback to the original logic
        if override_locale:
            request.state.babel.locale = override_locale
        else:
            request.state.babel.locale = self.get_language(request.state.babel, lang_code)

        # set the context var for template usage
        _context_var.set(request.state.babel.gettext)

        # optionally install jinja support
        if self.jinja2_templates:
            request.state.babel.install_jinja(self.jinja2_templates)

        response: Response = await call_next(request)
        return response
