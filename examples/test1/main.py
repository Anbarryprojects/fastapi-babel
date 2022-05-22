from fastapi import FastAPI, Request

from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel import _
from fastapi_babel.middleware import (
    InternationalizationMiddleware as I18nMiddleware
    )


configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)

app = FastAPI()
app.add_middleware(I18nMiddleware, babel=babel)

@app.get("/items/{id}")
async def read_item(request: Request, id: str):
    return {
        "id": id, 
        "message": _("Hello World"), 
        "locale": request.headers.get("Accept-Language")
        }