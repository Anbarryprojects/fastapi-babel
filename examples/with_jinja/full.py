from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_babel import _  # noqa
from fastapi_babel import Babel, BabelConfigs


app = FastAPI()
babel_configs = BabelConfigs(
        ROOT_DIR=__file__,
        BABEL_DEFAULT_LOCALE="en",
        BABEL_TRANSLATION_DIRECTORY="lang",
)
templates = Jinja2Templates(directory="templates")
app.add_middleware(BabelMiddleware, babel_configs=babel_configs, jinja2_templates=templates)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


if __name__ == "__main__":
    Babel(configs=babel_configs).run_cli()
