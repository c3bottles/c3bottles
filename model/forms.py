from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    back = HiddenField("back")
    args = HiddenField("args")
