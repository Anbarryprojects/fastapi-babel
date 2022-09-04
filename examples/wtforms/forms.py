from i18n import _
from wtforms import Form, StringField, validators as v
from wtforms import SubmitField


class lazy_gettext:
    def __init__(self, message) -> None:
        self.message = message

    def __repr__(self) -> str:
        return _(self.message)


class RegistrationForm(Form):
    username = StringField(
        lazy_gettext(_("Name")),
        [v.InputRequired(lazy_gettext(_("Please provide your name")))],
    )
    submit = SubmitField(lazy_gettext(_("Submit")))
