<p align="center">
  <img src="https://user-images.githubusercontent.com/56755478/165474515-12392df4-a41c-4ed9-bed4-512f606caedc.png" />
</p>




# FastAPI BABEL
### Get [pybabbel](https://github.com/python-babel/babel) tools directly within your FastAPI project without hassle.

FastAPI Babel is integrated within FastAPI framework and gives you support of i18n, l10n, date and time locales, and all other pybabel functionalities.

## Features:
- **I18n** (Internationalization)
- **Wtform Translation** (Lazy Text)
- **l10n** (Localization)
- **Date and time** locale
- **Decimal, Number** locale
- **Money and currency** locale converter
- locale selector from **HTTP header**

## Support
**Python:** 3.6 and later (tested on Python 3.6, 3.12)
**FastAPI**: 0.45.0 +
**PyBabel**: All

## Installation
    pip install fastapi-babel

# How to use

1. install FastAPI and FastAPI Babel:

`pip install fastapi`

and

`pip install fastapi_babel`

2. make `babel.py` file:

```python
from fastapi_babel import Babel, BabelConfigs

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)

if __name__ == "__main__":
    babel.run_cli()
```

3. make `babel.cfg` file

*babel.cfg*

    [python: **.py]


4. Create main.py file:

```python
from fastapi_babel import Babel, BabelConfigs, _

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

5. Extract the message <a name="step5"></a>

`pybabel extract -F babel.cfg -o messages.pot .`

6. Initialize pybabel

`pybabel init -i messages.pot -d lang -l fa`

7. Goto *lang/**YOUR_LANGUAGE_CODE**/LC_MESSAGES/messages.po* and **add your translation** to your messages.

8. Go back to the root folder and   Compile

`pybabel compile -d lang`

9. Run `main.py`

`python3 main.py`

- ### FastAPI Babel Commands
Install click at first:
`pip install click`

1. Add this snippet to your FasAPI code:

```python
...
babel.run_cli()
...
```
2. Now just follow the documentation from [step 5](#step5).

For more information just take a look at help flag of `main.py`
`python main.py --help`


#### Why FastAPI Babel CLI is recommanded ?
FastAPI Babel CLI will eliminate the need of concering the directories and paths, so you can concentrate on the project and spend less time on going forward and backward. You only need to specify **domain name**, **babel.cfg** and **localization directory**.


**NOTICE:** Do **not** use `FastAPI Babel` beside fastapi runner files (`main.py` or `run.py`), as uvicorn cli will not work.


[========]

## Using FastAPI Babel in an API

- create file `babel.py` and write the code below.

```python
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware 

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
app.add_middleware(BabelMiddleware, babel_configs=configs)

if __name__ == "__main__":
    Babel(configs).run_cli()
```
1. extract messages with following command

`python3 babel.py extract -d/--dir {watch_dir}`


**Notice: ** watch_dir is your project root directory, where the messages will be extracted.

2. Add your own language locale directory, for instance `fa`.

`python3 babel.py init -l fa`

3. Go to ./lang/Fa/.po and add your translations.

4. compile all locale directories.
`python3 babel.py compile`

```python
from fastapi import FastAPI


from fastapi_babel import _
from fastapi_babel import Babel, BabelConfigs
from fastapi_babel import BabelMiddleware

app = FastAPI()
babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
app.add_middleware(BabelMiddleware, babel_configs=babel_configs)


@app.get("/")
async def index():
    return {"text": _("Hello World")}


if __name__ == "__main__":
    Babel(configs=babel_configs).run_cli()

```

5. Now you can control your translation language from the request header and the locale code. The parameter is `Accept-Language`.

### How to use Jinja In FastAPI Babel

1. Add jinja extension to **babel.cfg**


```xml
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

2. Here is how your `main.py` should look like.


*main.py*

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from fastapi_babel import _
from fastapi_babel import Babel, BabelConfigs
from fastapi_babel import BabelMiddleware

app = FastAPI()
babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    BabelMiddleware, babel_configs=babel_configs, jinja2_templates=templates
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return {"text": _("Hello World")}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


if __name__ == "__main__":
    Babel(configs=babel_configs).run_cli()

```
3. Here is sample `index.html` file

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

4. Now just follow the documentation from [step 5](#step5).

5. More features like lazy gettext, please check the [Wtform Example](https://github.com/Anbarryprojects/fastapi-babel/tree/main/examples/wtforms)

### How to use multithread mode for fastapi babel:

```python

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


```

## Authors

- [@Parsa Pourmhammad](https://github.com/Legopapurida)


## Contributing

Contributions are always welcome!

Please read `contributing.md` to get familiar how to get started.

Please adhere to the project's `code of conduct`.


## Feedback And Support

Please open an issue and follow the template, so the community can help you.
