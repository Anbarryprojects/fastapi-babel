from babel_config import _ 
from babel_config import babel
 
if __name__ == "__main__":
    babel.locale = "en"
    en_text = _("Hello World")
    print(en_text)
    babel.locale = "fa"
    fa_text = _("Hello World")
    print(fa_text)
    babel.locale = "fr"
    fr_text = _("Hello World")
    print(fr_text)
    babel.locale = "es"
    es_text = _("Hello World")
    print(es_text)