from __future__ import annotations
from typing import Any


from fastapi import Request

from .core import Babel
from .local_context import context_var


def _(message: str) -> str:
    gettext = context_var.get()
    if not gettext:
        Babel.raise_context_error()
    return gettext(message)


class LaxyTextMeta(type):
    def __call__(cls, *args: Any, **kwds: Any) -> str:
        return super().__call__(*args, **kwds)


class LazyText(metaclass=LaxyTextMeta):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return _(self.message)


def use_babel(request: Request):
    """translate the message and retrieve message from .PO and .MO depends on
    `Babel.locale` locale.

    Args:
        message (str): message content

    Returns:
        str: transalted message.
    """
    # Get Babel instance from request or fallback to the CLI instance (when defined)
    babel = request.state.babel
    return babel
