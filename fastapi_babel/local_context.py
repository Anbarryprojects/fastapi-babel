from __future__ import annotations

from contextvars import ContextVar
import logging
from typing import Any, Callable, Type
import typing


from .properties import RootConfigs
from .core import Babel
from .properties import RootConfigs


class BabelContext:
    def __init__(
        self,
        babel_config: RootConfigs,
        babel: typing.Optional[Babel] = None,
        logger: typing.Optional[logging.Logger] = None,
        do_log: bool = False,
    ) -> None:
        """Babel context to insert object into `ContextVar`.

        Args:
            babel_config (RootConfigs): Base config object
            logger (typing.Optional[Logger], optional): Logger object to log inside of context manager scope.
            Defaults to None.
        """
        self.babel_config = babel_config
        self.logger = logger or logging.getLogger()
        self.__babel = babel or Babel(self.babel_config)
        self.do_log = do_log

    def _log(self, error: Exception, *msg: typing.Tuple[Any]):
        """default log method

        Args:
            error (Exception): raised error inside context manager scope.
        """
        self.logger.error(error, *msg, exc_info=True)

    def __enter__(self):
        context_var.set(self.__babel.gettext)

    def __exit__(self, *args, **kwargs): ...


context_var: ContextVar[Callable[[str], str]] = ContextVar("gettext")
