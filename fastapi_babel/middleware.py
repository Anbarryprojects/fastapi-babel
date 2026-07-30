import re
from collections.abc import Callable
from pathlib import Path
from typing import Optional

from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.datastructures import State
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send

from .core import Babel
from .local_context import context_var
from .properties import RootConfigs

LANGUAGES_PATTERN = re.compile(r"([a-z]{2})-?([A-Z]{2})?(;q=\d.\d{1,3})?")


class BabelMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        babel_configs: RootConfigs,
        locale_selector: Optional[Callable[[Request], Optional[str]]] = None,
        jinja2_templates: Optional[Jinja2Templates] = None,
    ) -> None:
        self.app = app
        self.babel_configs = babel_configs
        self.jinja2_templates = jinja2_templates
        self.locale_selector = locale_selector or self._default_locale_selector

    def _default_locale_selector(self, conn: HTTPConnection[State]) -> Optional[str]:
        return conn.headers.get("Accept-Language", None)

    def get_language(self, babel: Babel, lang_code: Optional[str] = None) -> str:
        """Applies an available language.

        To apply an available language it will be searched in the language folder for an available one
        and will also priotize the one with the highest quality value. The Fallback language will be the
        taken from the BABEL_DEFAULT_LOCALE var.

            Args:
                babel (Babel): Request scoped Babel instance
                lang_code (str): The Value of the Accept-Language Header.

            Returns:
                str: The language that should be used.
        """
        if not lang_code:
            return babel.config.BABEL_DEFAULT_LOCALE

        matches = re.finditer(LANGUAGES_PATTERN, lang_code)
        languages = [(f"{m.group(1)}{f'_{m.group(2)}' if m.group(2) else ''}", m.group(3) or "") for m in matches]
        languages = sorted(languages, key=lambda x: x[1], reverse=True)  # sort the priority, no priority comes last
        translation_directory = Path(babel.config.BABEL_TRANSLATION_DIRECTORY)
        translation_files = [i.name for i in translation_directory.iterdir()]
        explicit_priority = None

        for lang, quality in languages:
            if lang in translation_files:
                if not quality:  # languages without quality value having the highest priority 1
                    return lang

                if not explicit_priority:  # set language with explicit priority <= priority 1
                    explicit_priority = lang

        # Return language with explicit priority or default value
        return explicit_priority or self.babel_configs.BABEL_DEFAULT_LOCALE

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        lang_code: Optional[str] = self.locale_selector(conn)

        # Create a new Babel instance per request
        babel = Babel(configs=self.babel_configs)
        babel.locale = self.get_language(babel, lang_code)
        context_var.set(babel.gettext)
        if self.jinja2_templates:
            babel.install_jinja(self.jinja2_templates)

        conn.state.babel = babel

        await self.app(scope, receive, send)

