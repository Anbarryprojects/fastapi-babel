from fastapi import APIRouter
from fastapi import Request
from i18n import babel, _
from app import Application as root
from forms import RegistrationForm
from gettext import find

router = APIRouter(prefix="")
render = root.templates.TemplateResponse


@router.get("/")
async def read_item(request: Request):
    form = RegistrationForm()
    babel.locale = "fa"
    return render("index.html", {"request": request, "form": form})


@router.post("/")
async def read_item(request: Request):
    form = RegistrationForm(await request.form())
    babel.locale = "fa"
    if form.validate():
        return render("index.html", {"request": request, "form": form})
    return form.errors
