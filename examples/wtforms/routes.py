from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import Request
from app import Application as root
from fastapi_babel.core import Babel
from fastapi_babel.helpers import use_babel
from fastapi_babel.local_context import BabelContext
from forms import RegistrationForm
from i18n import babel_config

router: APIRouter = APIRouter(prefix="")
render = root.templates.TemplateResponse


@router.get("/")
async def read_item(request: Request, babel: Annotated[Babel, Depends(use_babel)]):
    babel.locale = "fa"
    # with BabelContext(babel_config, babel=babel):
    form = RegistrationForm()
    return render("index.html", {"request": request, "form": form})


@router.post("/")
async def send_item(request: Request):
    form = RegistrationForm(await request.form())
    if form.validate():
        return render("index.html", {"request": request, "form": form})
    return form.errors
