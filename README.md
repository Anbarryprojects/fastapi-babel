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


## Using FastAPI Babel in an API


