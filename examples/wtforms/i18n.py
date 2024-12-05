from fastapi_babel import Babel
from fastapi_babel import BabelCli
from fastapi_babel import BabelConfigs
from fastapi_babel import _

babel_config = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=babel_config)

if __name__ == "__main__":
    babel_cli = BabelCli(babel)
    babel_cli.run()
