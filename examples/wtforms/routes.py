from fastapi import APIRouter
from fastapi import Request
from i18n import babel, _
from app import Application as root
from forms import RegistrationForm

router: APIRouter = APIRouter(prefix="")
render = root.templates.TemplateResponse


@router.get("/")
async def read_item(request: Request):
    form = RegistrationForm()
    return render("index.html", {"request": request, "form": form})


@router.post("/")
async def send_item(request: Request):
    form = RegistrationForm(await request.form())
    if form.validate():
        return render("index.html", {"request": request, "form": form})
    return form.errors
