def check_jinja_import():
    try:
        import jinja2  # noqa
    except ImportError:
        raise ImportError(
            """
            Jinja2 has not installed.
        """
        ) from ImportError


def check_click_import():
    try:
        import click  # noqa
    except ImportError:
        raise ImportError(
            """
            click has not installed.
        """
        ) from ImportError
