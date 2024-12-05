from i18n import _
from fastapi_babel import lazy_gettext as _
from wtforms import Form, StringField, validators as v
from wtforms import SubmitField


class RegistrationForm(Form):
    username = StringField(
        _("Name"),
        [v.InputRequired(_("Please provide your name"))],
    )
    submit = SubmitField(_("Submit"))
