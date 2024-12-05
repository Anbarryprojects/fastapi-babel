from __future__ import annotations

from subprocess import run
from typing import Optional
from .core import Babel


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
        try:
            from click import echo, group, option
        except ImportError:
            raise ImportError("click has not installed.")

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
        def extract(dir: str):
            """Extract messages

            Args:
                dir (Optional[str], optional): directory to extract messages. Defaults to None.
            """

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

        self.__all__ = [update, compile, init, extract]
        cmd()
