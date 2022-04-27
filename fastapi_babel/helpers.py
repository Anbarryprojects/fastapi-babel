def check_jinja_import():
    try:
        import jinja2
    except ImportError as err:
        raise ImportError("""
            Jinja2 has not installed.
        """) from ImportError

def check_click_import():
    try:
        import click
    except ImportError as err:
        raise ImportError("""
            click has not installed.
        """) from ImportError
