from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, HiddenField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    back = HiddenField("back")
    args = HiddenField("args")


class UserIdForm(FlaskForm):
    user_id = IntegerField("user_id", widget=HiddenInput())


class PermissionsForm(UserIdForm):
    can_visit = BooleanField("can_visit")
    can_edit = BooleanField("can_edit")
    is_admin = BooleanField("is_admin")


class PasswordForm(UserIdForm):
    password_1 = PasswordField("password_1", validators=[DataRequired()])
    password_2 = PasswordField("password_2", validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    can_visit = BooleanField("can_visit")
    can_edit = BooleanField("can_edit")
    is_admin = BooleanField("is_admin")
