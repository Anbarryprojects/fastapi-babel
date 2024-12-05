import threading
from typing import Annotated
from i18n import _
from i18n import babel_configs
from fastapi import Depends, FastAPI
from fastapi_babel import BabelMiddleware
from fastapi_babel.core import Babel, BabelContext, get_babel

app = FastAPI()
app.add_middleware(BabelMiddleware, babel_configs=babel_configs)


def translate_after(babel: Babel):
    with BabelContext(babel_configs, babel=babel):
        print(_("Hello world"))


@app.get("/")
async def index(babel: Annotated[Babel, Depends(get_babel)]):
    t = threading.Thread(target=translate_after, args=[babel])
    t.start()
    return {"text": "Bye"}
