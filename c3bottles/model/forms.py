from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, HiddenField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    back = HiddenField("back")
    args = HiddenField("args")


class DeleteUserForm(FlaskForm):
    user_id = IntegerField("user_id", widget=HiddenInput())
