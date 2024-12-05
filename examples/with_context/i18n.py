from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel import _


babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)


if __name__ == "__main__":
    babel: Babel = Babel(configs=babel_configs)
    babel.run_cli()
