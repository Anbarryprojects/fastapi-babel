from _babel import _ 
from _babel import babel
 
if __name__ == "__main__":
    babel.locale = "en"
    en_text = _("File not found. There is nothing here")
    print(en_text)
    babel.locale = "fa"
    fa_text = _("File not found. There is nothing here")
    print(fa_text)
    babel.locale = "fr"
    fr_text = _("File not found. There is nothing here")
    print(fr_text)
    babel.locale = "es"
    es_text = _("File not found. There is nothing here")
    print(es_text)