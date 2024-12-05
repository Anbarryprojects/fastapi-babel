import threading
from time import sleep
from typing import Annotated

from pydantic import BaseModel
from i18n import _
from i18n import babel_configs
from fastapi import Depends, FastAPI
from fastapi_babel import BabelMiddleware, Babel
from fastapi_babel.local_context import BabelContext
from fastapi_babel import use_babel

app = FastAPI()
app.add_middleware(BabelMiddleware, babel_configs=babel_configs)


class ResponseModel(BaseModel):
    idx: int
    text: str


def translate_after(idx, babel: Babel):
    with BabelContext(babel_configs, babel=babel):
        print(_("Hello world"), babel.locale, idx)


@app.get("/", response_model=ResponseModel)
async def index(idx: int, babel: Annotated[Babel, Depends(use_babel)]):
    t = threading.Thread(target=translate_after, args=[idx, babel])
    t.start()
    return ResponseModel(idx=idx, text=_("Hello world"))
