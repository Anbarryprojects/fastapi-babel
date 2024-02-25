from typing import Type
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from i18n import babel
from fastapi_babel.middleware import BabelMiddleware


class Application:
    app: FastAPI
    templates: Jinja2Templates


def create_app() -> FastAPI:
    root: Type[Application] = Application
    root.app = FastAPI()
    root.templates = Jinja2Templates(directory="templates")
    templates = Jinja2Templates(directory="templates")
    root.app.add_middleware(
        BabelMiddleware, babel_configs=babel.config, jinja2_templates=templates
    )
    from routes import router

    root.app.include_router(router=router)
    return root.app
