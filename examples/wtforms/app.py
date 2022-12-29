from typing import Type
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from i18n import babel


class Application:
    app: FastAPI
    templates: Jinja2Templates


def create_app() -> FastAPI:
    root: Type[Application] = Application
    root.app = FastAPI()
    root.templates = Jinja2Templates(directory="templates")
    babel.init_app(app=root.app)
    babel.install_jinja(root.templates)
    from routes import router

    root.app.include_router(router=router)
    return root.app
