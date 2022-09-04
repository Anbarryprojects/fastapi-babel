<p align="center">
  <img src="https://user-images.githubusercontent.com/56755478/165474515-12392df4-a41c-4ed9-bed4-512f606caedc.png" />
</p>




# FastAPI BABEL
### Get [pybabbel](https://github.com/python-babel/babel) tools directly within your FastAPI project without hassle.

FastAPI Babel is will be integrated within FastAPI framework and gives you support of i18n, l10n, date and time locales and all other pybabel functionalities.

## Features:
- **I18n** (Internationalization)
- **Wtform Translation** (Lazy Text)
- **l10n** (Localization)
- **Date and time** locale
- **Decimal, Number** locale
- **Money and currency** locale converter
- locale selector from **http header**

## Support
**Python:** 3.6 and later (tested on Python 3.6, 3.7, 3.8, and 3.9)
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

3. make `babel.cfg` file

*babel.cfg*

    [python: **.py]


4. Create main.py file:

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

5. Extract the massage <a name="step5"></a>

`pybabel extract -F babel.cfg -o messages.pot .`

6. Initialize pybabble

`pybabel init -i messages.pot -d lang -l fa`

7. Goto *lang/**YOUR_LANGUAGE_CODE**/LC_MESSAGES/messages.po* and **add your translation** to your messages.

8. Go back to the root folder and   Compile

`pybabel compile -d lang`

9. Run `main.py`

`python3 main.py`

10. Enjoy

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
FastAPI Babel CLI will eliminate the need of concering the directories and paths, so you can concentrate on the project and spend less time on going forward and backward. You only need to specify **domain name**, **babel.cfg** and** localization directory **.

**NOTICE:** Do **not** use `FastAPI Babbel` beside fastapi runner files (`main.py` or `run.py`), as uvicorn cli will not work.


[========]

## Using FastAPI Babel in an API

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
1. Extract messages with following command

`python3 babel.py extract -d/--dir {watch_dir}`

**Notice: ** watch_dir is your project root directory, or where you want to extract the messages into that directory.

2. add your own langauge locale directory, for instance `fa`.

`python3 babel.py init -l fa`

3. go to ./lang/Fa/.po and add your translations.

4. compile all locale directorties.
`python3 babel.py compile`

```python
from fastapi import FastAPI, Request
from fastapi_babel import _
from .babel import babel

app = FastAPI()
babel.init_app(app)

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return id + _("Hello World")

```

5. Now you can control your translation langauge from header of request and locale code. The parameter is `Accept-Laguage`.

Screenshot:
[![Screenshot 1](https://user-images.githubusercontent.com/56755478/169701538-8f893d0e-fd09-4004-8e8d-5e045a1d588a.png "Screenshot 1")](https://user-images.githubusercontent.com/56755478/169701538-8f893d0e-fd09-4004-8e8d-5e045a1d588a.png "Screenshot 1")

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

from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel import _

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="lang",
)

app = FastAPI()
babel = Babel(app, configs=configs)
babel.install_jinja(templates)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
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

## Authors

- [@Parsa Pourmhammad](https://github.com/Legopapurida)


## Contributing

Contributions are always welcome!

Please read `contributing.md` to get familiar how to get started.

Please adhere to the project's `code of conduct`.


## Feedback And Support

Please open an issue and follow the template, so the community can help you.
