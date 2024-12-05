from __future__ import annotations

from gettext import gettext, translation
from typing import Any, Callable, NoReturn, Optional

from fastapi.templating import Jinja2Templates


from .properties import RootConfigs
from .exceptions import BabelProxyError
from contextvars import ContextVar, Token


class Babel:

    def __init__(self, configs: RootConfigs) -> None:
        """
        `Babel` is manager for babel localization
            and i18n tools like gettext, translation, ...

        Args:
            configs (RootConfigs): Babel configs for using.
        """
        self.config: RootConfigs = configs
        self.__locale: str = self.config.BABEL_DEFAULT_LOCALE
        self.__default_locale: str = self.config.BABEL_DEFAULT_LOCALE
        self.__domain: str = self.config.BABEL_DOMAIN.split(".")[0]

    @staticmethod
    def raise_context_error() -> NoReturn:
        raise BabelProxyError(
            "Babel instance is not available in the current request context."
        )

    @property
    def domain(self) -> str:
        return self.__domain

    @property
    def default_locale(self) -> str:
        return self.__default_locale

    @property
    def locale(self) -> str:
        return self.__locale

    @locale.setter
    def locale(self, value: str) -> None:
        self.__locale = value

    @property
    def gettext(self) -> Callable[[str], str]:
        if self.default_locale != self.locale:
            gt = translation(
                self.domain,
                self.config.BABEL_TRANSLATION_DIRECTORY,
                [self.locale],
            )
            gt.install()
            return gt.gettext
        return gettext

    def install_jinja(self, templates: Jinja2Templates) -> None:
        """
        `Babel.install_jinja` install gettext to jinja2 environment
            to access `_` in whole
            the jinja templates and let it to pybabel for
            extracting included messages throughout the templates.

        Args:
            templates (Jinja2Templates): Starlette Jinja2Templates object.
        """
        from .helpers import _

        try:
            from jinja2 import Environment  # type: ignore # noqa
        except ImportError:
            raise ImportError(
                """
                Jinja2 has not installed.
            """
            ) from ImportError

        self.env: Environment = getattr(templates, "env", Environment())
        globals: dict[str, Any] = getattr(self.env, "globals", dict())
        globals.update({"_": _})

    def run_cli(self):
        """installs cli's for using pybabel commands easily by specified
        configs from `BabelConfigs`.
        """

        from .cli import BabelCli  # type: ignore # noqa

        babel_cli = BabelCli(self)
        babel_cli.run()
