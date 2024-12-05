from __future__ import annotations

from gettext import gettext, translation
from logging import Logger
from subprocess import run
from typing import Callable, Optional
import typing

from fastapi import Request
from fastapi.templating import Jinja2Templates

from .helpers import check_click_import, check_jinja_import
from .properties import RootConfigs
from .exceptions import BabelProxyError
from contextvars import ContextVar


class Babel:

    instance: Optional[Babel] = None  # Singleton used by Babel CLI

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
        check_jinja_import()
        from jinja2 import Environment

        self.env: Environment = templates.env
        globals: dict = self.env.globals
        globals.update({"_": _})

    def run_cli(self):
        """installs cli's for using pybabel commands easily by specified
        configs from `BabelConfigs`.
        """
        check_click_import()
        babel_cli = BabelCli(self)
        babel_cli.run()


class __LazyText:
    def __init__(self, message) -> None:
        self.message = message

    def __repr__(self) -> str:
        return _(self.message)


def make_gettext(request: Request) -> Callable[[str], str]:
    def translate(message: str) -> str:
        """translate the message and retrieve message from .PO and .MO depends on
        `Babel.locale` locale.

        Args:
            message (str): message content

        Returns:
            str: transalted message.
        """
        # Get Babel instance from request or fallback to the CLI instance (when defined)
        babel = getattr(request.state, "babel", Babel.instance)
        if babel is None:
            raise BabelProxyError(
                "Babel instance is not available in the current request context."
            )

        return babel.gettext(message)

    return translate


def get_babel(request: Request) -> Babel:
    """Get the babel object from request context in state of each income scope

    Args:
        request (Request): request object

    Returns:
        Babel: babel object
    """

    babel = getattr(request.state, "babel", Babel.instance)
    if babel is None:
        raise BabelProxyError(
            "Babel instance is not available in the current request context."
        )

    return babel


_context_var: ContextVar[Callable[[str], str]] = ContextVar("gettext")


class BabelContext:
    def __init__(
        self,
        babel_config: RootConfigs,
        babel: typing.Optional[Babel] = None,
        logger: typing.Optional[Logger] = None,
    ) -> None:
        """Babel context to insert object into `ContextVar`.

        Args:
            babel_config (RootConfigs): Base config object
            logger (typing.Optional[Logger], optional): Logger object to log inside of context manager scope.
            Defaults to None.
        """
        self.babel_config = babel_config
        self.logger = logger
        self.__babel = babel

    def _log(self, error: Exception):
        """default log method

        Args:
            error (Exception): raised error inside context manager scope.
        """
        self.logger.error(error, exc_info=True)

    def __enter__(self):
        babel = self.__babel or Babel(self.babel_config)
        _context_var.set(babel.gettext)
        return babel

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.logger:
            self._log(exc_value)
        return True


def _(message: str) -> str:
    gettext = _context_var.get()
    return gettext(message)


lazy_gettext = __LazyText


class BabelCli:
    __module_name__ = "pybabel"

    def __init__(self, babel: Babel) -> None:
        """Babel cli manager to facilitate using pybabel commands by specified congigs
        fron `BabelConfigs`.

        Args:
            babel (Babel): `Babel` instance
        """
        self.babel = babel

    def extract(self, watch_dir: str) -> None:
        """extract all messages that annotated using gettext/_
        in the specified directory.

        for first time will create messages.pot file into the root
        directory.

        Args:
            watch_dir (str): directory to extract messages.
        """
        run(
            [
                BabelCli.__module_name__,
                "extract",
                "-F",
                self.babel.config.BABEL_CONFIG_FILE,
                "-o",
                self.babel.config.BABEL_MESSAGE_POT_FILE,
                watch_dir,
            ]
        )

    def init(self, lang: Optional[str] = None) -> None:
        """Initialized lacale directory for first time.
        if there is already exists the directory, notice that your
        all comiled and initialized messages will remove, in this
        condition has better to use `Babel.update` method.

        Args:
            lang (str): locale directory name and path
        """
        run(
            [
                BabelCli.__module_name__,
                "init",
                "-i",
                self.babel.config.BABEL_MESSAGE_POT_FILE,
                "-d",
                self.babel.config.BABEL_TRANSLATION_DIRECTORY,
                "-l",
                lang or self.babel.config.BABEL_DEFAULT_LOCALE,
            ]
        )

    def update(self, watch_dir: Optional[str] = None) -> None:
        """update the extracted messages after init command/initialized directory
        , Default is `./lang`"

        Args:
            watch_dir (str): locale directory name and path
        """
        run(
            [
                BabelCli.__module_name__,
                "update",
                "-i",
                self.babel.config.BABEL_MESSAGE_POT_FILE,
                "-d",
                watch_dir or self.babel.config.BABEL_TRANSLATION_DIRECTORY,
            ]
        )

    def compile(self):
        """
        compile all messages from translation directory in .PO to .MO file and is
        a binnary text file.
        """
        run(
            [
                BabelCli.__module_name__,
                "compile",
                "-d",
                self.babel.config.BABEL_TRANSLATION_DIRECTORY,
            ]
        )

    def run(self):
        from click import echo, group, option

        @group(
            "cmd",
            help="""
            First Step to extracting messages:\n

                1- extract -d/--dir {watch_dir}\n
                2- init -l/--lang {lang}\n
                3- add your custome translation to your lang `.po` file for example FA dir {./lang/fa}. \n
                4- compile.\n

                Example: \n
                    1- extract -d .\n
                    2- init -l fa\n
                    3- go to ./lang/Fa/.po and add your translations.\n
                    4- compile\n

            If you have already extracted messages and you have an existing `.po` and `.mo` file
            follow this steps:\n
                1- extract -d/--dir {watch_dir} \n
                2- update -d/--dir {lang_dir} defaults is ./lang \n
                3- add your custome to your lang `.po` file for example FA dir {./lang/fa}. \n
                4- compile.

                Example: \n
                    1- extract -d .\n
                    2- update -d lang\n
                    3- go to ./lang/Fa/.po and add your translations.\n
                    4- compile\n
        """,  # noqa
        )
        def cmd():
            pass

        @cmd.command(
            "extract",
            help="""extract all messages that annotated using gettext/_
                in the specified directory.

                for first time will create messages.pot file into the root
                directory.""",
        )
        @option("-d", "--dir", "dir", help="watch dir")
        def extract(dir):
            try:
                self.extract(dir)
            except Exception as err:
                echo(err)

        @cmd.command(
            "init",
            help="""Initialized lacale directory for first time.
                if there is already exists the directory, notice that your
                all comiled and initialized messages will remove, in this
                condition has better to use `update` command""",
        )
        @option(
            "-l",
            "--lang",
            "lang",
            help="locale directory name and path, default is fa",
            default="fa",
        )
        def init(lang: Optional[str] = None):
            try:
                self.init(lang)
            except Exception as err:
                echo(err)

        @cmd.command(
            "compile",
            help="""compile all messages from translation directory in .PO to .MO file and is
                a binnary text file.""",
        )
        def compile():
            try:
                self.compile()
            except Exception as err:
                echo(err)

        @cmd.command(
            "update",
            help="""update the extracted messages after init command/initialized directory
                , Default is `./lang`""",
        )
        @option("-d", "--dir", "dir", help="locale directory name and path")
        def update(dir: Optional[str] = None):
            try:
                self.update(dir)
            except Exception as err:
                echo(err)

        cmd()
