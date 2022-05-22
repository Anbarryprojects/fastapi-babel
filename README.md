![](https://user-images.githubusercontent.com/56755478/165474515-12392df4-a41c-4ed9-bed4-512f606caedc.png)


# FastAPI BABEL
Fastapi babel is a tool what supports i18n, l10n, date and time locales and all pybabel functionalities easily that integrated with fastapi framework.

## Features:
- **I18n** (Internationalization)
- **l10n** (Localization)
- **Date and time** locale
- **Decimal, Number** locale
- **Money and currency** locale converter
- locale selector from **http header**

## Support
**Python:** 3.6 and later (tested against 3.6, 3.7, 3.8 and 3.9)
**FastAPI**: 0.45.0 +
**PyBabel**: All

## Installation
    pip install fastapi-babel

# How to use FastAPI Babel?
- Create main.py file:

```python
from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel import _

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)
    
def main():
    babel.locale = "en"
    en_text = _("Hello World")
    print(en_text)

    babel.locale = "fa"
    fa_text = _("Hello World")
    print(fa_text)

if __name__ == "__main__":
    main()
```

- ### PyBabel Commands
1. extracting
`pybabel extract -F babel.cfg -o messages.pot .`

2. initializing
`pybabel init -i messages.pot -d lang -l fa`

3. Goto *lang/fa/LC_MESSAGES/messages.po* and add your translation to your messages.

4. compiling
`pybabel compile -d lang`

- ### FastAPI Babel Commands
Install click at first:
`pip install click`

Add this snippet to your code:

```python
...
babel.run_cli()
...
```
Now you can follow those part of mentioned above for message extracting process.
**For more information your can check helpers of babel cli:
**
`python main.py --help`

#### Why FastAPI Babel Cli is recommanded ?
when you are creating application in a production level where you will deploy it on a server you may not found the right directory and paths of babel domain and config files, but FastAPI Babel Cli will do it perfectly without any concern about that. you only need to specify **domain name**, **babel.cfg** and** localization directory **.

**NOTICE:** you never use it beside of fastapi runner file line `main.py` or `run.py`, because uvicorn cli will not work anymore.

You have better to seperate a babel cli runner file beside of fastapi runner file, by the way you will not overwhelm with failure at uvicorn cli.


[========]

## Using FastAPI Babel in an API
First of all we have to extract, translate and compile the messages, so follow the steps.

Notice: first of all you should create a babel config file **babel.cfg** in project root or where you want to run cli's.

*babel.cfg*

    [python: **.py]


- create file `babel.py` and write the code below.

```python
from fastapi_babel import Babel
from fastapi_babel import BabelConfigs

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)

if __name__ == "__main__":
    babel.run_cli()
```
- extract messages with following command

`python3 babel.py extract -d/--dir {watch_dir}`

**Notice: ** watch_dir can be your project directory or messages you want to extract that.

- add your own langauge locale directory such as fa by following commands.

`python3 babel.py init -l fa`

- go to ./lang/Fa/.po and add your translations.
- compile all locale directorties.
`python3 babel.py compile`

```python
from fastapi import FastAPI, Request
from fastapi_babel import _
from fastapi_babel.middleware import InternationalizationMiddleware as I18nMiddleware
from .babel import babel

app = FastAPI()
app.add_middleware(I18nMiddleware, babel=babel)

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return id + _("Hello World")

```

- Now you can control your translation langauge from header of request and locale code. the meant locale header param is **Accept-Laguage **.

Screenshot:
[![Screenshot 1](https://user-images.githubusercontent.com/56755478/169701538-8f893d0e-fd09-4004-8e8d-5e045a1d588a.png "Screenshot 1")](https://user-images.githubusercontent.com/56755478/169701538-8f893d0e-fd09-4004-8e8d-5e045a1d588a.png "Screenshot 1")

### How to use Jinja In FastAPI Babel

- Add jinja extension to **babel.cfg**


```xml
[python: **.py] 
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```


*main.py*

```python
from fastapi import FastAPI, Request

from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel import _
from fastapi_babel.middleware import InternationalizationMiddleware as I18nMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)
babel.install_jinja(templates)

app = FastAPI()
app.add_middleware(I18nMiddleware, babel=babel)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
```

*index.html*

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>{{_("Hello World")}}</h1>
</body>
</html>
```


- Repeat all steps that we explained above for extracting messages, ...


## Authors

- [@Parsa Pourmhammad](https://github.com/Legopapurida)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Feedback

If you have any feedback, please reach out to us at parsapourmohammad@gmail.com


## Support

For support, email parsapourmohammad1999@gmail.com.


