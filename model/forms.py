from flask import request
from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    back = HiddenField("back")
    args = HiddenField("args")
