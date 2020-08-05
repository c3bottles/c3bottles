from typing import Dict, Iterable, List, Optional, Union

import click
from flask import abort, current_app
from flask_babel import LazyString, lazy_gettext
from flask_login import AnonymousUserMixin, UserMixin
from pwgen import pwgen

from c3bottles import app, bcrypt, db, lm

MAXLENGTH_NAME = 128
MAXLENGTH_PW = 128
TOKEN_LENGTH = 128


class User(db.Model, UserMixin):
    """
    The User class represents a user that can access the web interface. Each
    user has a login (i.e. user name), a password and may have the right to
    visit drop points, to edit drop points or admin rights (i.e. adding or
    removing other users or changing their credentials).
    """

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(MAXLENGTH_NAME), nullable=False, unique=True)
    password = db.Column("password", db.LargeBinary, nullable=False)
    token = db.Column("token", db.String(TOKEN_LENGTH), nullable=False)
    can_visit = db.Column("can_visit", db.Boolean, nullable=False, default=True)
    can_edit = db.Column("can_edit", db.Boolean, nullable=False, default=False)
    is_admin = db.Column("is_admin", db.Boolean, nullable=False, default=False)
    is_active = db.Column("is_active", db.Boolean, nullable=False, default=True)
    must_reset_pw = db.Column("must_reset_pw", db.Boolean, nullable=False, default=True)

    def __init__(
        self,
        name: str = None,
        password: str = None,
        can_visit: bool = True,
        can_edit: bool = False,
        is_admin: bool = False,
        must_reset_pw: bool = True,
    ):

        errors: List[Dict[str, LazyString]] = []

        if not (name and password):
            errors.append({"user": lazy_gettext("User needs a name and a password.")})

        if not isinstance(name, str):
            errors.append({"user": lazy_gettext("User name is not a string.")})
        else:
            if len(name) > MAXLENGTH_NAME:
                errors.append({"user": lazy_gettext("User name is too long.")})

        try:
            self.password = bcrypt.generate_password_hash(password)
        except (TypeError, ValueError):
            errors.append({"user": lazy_gettext("Password hashing failed.")})

        self.name = name
        self.token = make_secure_token()
        self.can_visit = can_visit
        self.can_edit = can_edit
        self.is_admin = is_admin
        self.must_reset_pw = must_reset_pw

        if errors:
            raise ValueError(*errors)

        db.session.add(self)
        db.session.commit()

    @property
    def user_id(self) -> int:
        return self._id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def can_report(self) -> bool:
        return True

    def get_id(self) -> str:
        return self.token

    def validate_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def get(cls, _id: Union[int, str]) -> Optional["User"]:
        """
        Get a user by their id or name from the database.

        :param _id: the id (as an int) or name (as a str) of the user to get
        :return: the user object in question or :class:`None` if no user
            exists with the given id or name
        """
        if isinstance(_id, int):
            return cls.query.get(_id)
        elif isinstance(_id, str):
            return cls.query.filter(cls.name == _id).first()

    @classmethod
    def get_or_404(cls, _id: Union[int, str]) -> "User":
        """
        Get a user by their id or name from the database. If the user does not exist,
        abort the current request with an error 404.

        :param _id: the id (as an int) or name (as a str) of the user to get
        :return: the user object in question
        """

        if isinstance(_id, int):
            return cls.query.get_or_404(_id)
        elif isinstance(_id, str):
            return cls.query.filter(cls.name == _id).first_or_404()
        else:
            abort(404)

    @classmethod
    def get_by_token(cls, token: str) -> Optional["User"]:
        """
        Get a user by their token from the database.

        :param token: The token of the user to get.
        :return: the user object in question or :class:`None` if no
            user exists with the token given
        """
        return User.query.filter(User.token == token).first()

    @classmethod
    def all(cls) -> Iterable["User"]:
        """
        Get all users from the database.

        :return: a list of all users in the database
        """
        return cls.query.all()


@lm.user_loader
def load_(token) -> Optional[User]:
    return User.get_by_token(token)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        pass

    @property
    def name(self) -> LazyString:
        return lazy_gettext("Unknown")

    @property
    def user_id(self) -> int:
        return 0

    @property
    def can_report(self) -> bool:
        return not current_app.config.get("NO_ANONYMOUS_REPORTING", False)

    @property
    def can_visit(self) -> bool:
        return False

    @property
    def can_edit(self) -> bool:
        return False

    @property
    def is_admin(self) -> bool:
        return False


lm.anonymous_user = Anonymous


def make_secure_token() -> str:
    """
    Generate a session token by which the user session will be identified.
    This is tied to the account and allows getting the account from a session
    cookie.

    :return: a random token
    """
    return pwgen(TOKEN_LENGTH, no_symbols=True)


@app.cli.group("user")
def user_management():
    """
    User management.

    These commands allow creation, deletion etc. of users.
    """


@user_management.command("create")
@click.option("--name", prompt="User name")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--can-visit", prompt="Can the user visit drop points?", is_flag=True)
@click.option("--can-edit", prompt="Can the user edit drop points?", is_flag=True)
@click.option("--admin", prompt="Is the user an administrator?", is_flag=True)
def create_user(name: str, password: str, can_visit: bool, can_edit: bool, admin: bool):
    """
    Creates a new user.
    """
    if User.get(name) is not None:
        print("A user with the name {} already exists!".format(name))
        exit(1)
    else:
        User(name, password, can_visit, can_edit, admin, False)
        print("User created successfully.")


@user_management.command("delete")
@click.option("--name", prompt="User name")
def delete_user(name: str):
    """
    Deletes a user.
    """
    u = User.get(name)
    if u is None:
        print("ERROR: The user {} does not exist!".format(name))
        exit(1)
    else:
        db.session.delete(u)
        db.session.commit()


@user_management.command("password")
@click.option("--name", prompt="User name")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def change_password(name: str, password: str):
    """
    Sets a new password for a user.
    """
    u = User.get(name)
    if u is None:
        print("ERROR: The user {} does not exist!".format(name))
        exit(1)
    else:
        u._password = bcrypt.generate_password_hash(password)
        print("Password for {} changed successfully.".format(name))


@user_management.command("list")
def list_users():
    """
    Lists all users.
    """
    for user in User.all():
        s = "{} (user id {})".format(user.name, user.user_id)
        if user.can_visit:
            s += ", can visit drop points"
        if user.can_edit:
            s += ", can edit drop points"
        if user.is_admin:
            s += ", is admin"
        print(s)
