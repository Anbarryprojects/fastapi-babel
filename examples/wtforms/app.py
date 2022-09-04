from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from i18n import babel


class Application:
    app: FastAPI = None
    templates: Jinja2Templates = None


def create_app() -> FastAPI:
    root = Application
    root.app = FastAPI()
    root.templates = Jinja2Templates(directory="templates")
    babel.init_app(app=root.app)
    babel.install_jinja(root.templates)
    from routes import router

    root.app.include_router(router=router)
    return root.app
