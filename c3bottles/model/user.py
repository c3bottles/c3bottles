from pwgen import pwgen

from flask_login import UserMixin, AnonymousUserMixin
from flask_babel import lazy_gettext as _

from .. import db, lm, bcrypt


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
    name = db.Column("name", db.String(MAXLENGTH_NAME), nullable=False,
                     unique=True)
    _password = db.Column("password", db.LargeBinary, nullable=False)
    _token = db.Column("token", db.String(TOKEN_LENGTH), nullable=False)
    can_visit = db.Column("can_visit", db.Boolean, nullable=False, default=True)
    can_edit = db.Column("can_edit", db.Boolean, nullable=False, default=False)
    is_admin = db.Column("is_admin", db.Boolean, nullable=False, default=False)
    is_active = db.Column("is_active", db.Boolean, nullable=False, default=True)
    must_reset_pw = db.Column("must_reset_pw", db.Boolean, nullable=False,
                              default=True)

    def __init__(self, name=None, password=None, can_visit=True, can_edit=False,
                 is_admin=False, must_reset_pw=True):

        errors = []

        if not (name and password):
            errors.append({"user": _("User needs a name and a password.")})

        if not isinstance(name, str):
            errors.append({"user": _("User name is not a string.")})
        else:
            if len(name) > MAXLENGTH_NAME:
                errors.append({"user": _("User name is too long.")})

        try:
            self._password = bcrypt.generate_password_hash(password)
        except (TypeError, ValueError):
            errors.append({"user": _("Password hashing failed.")})

        self.name = name
        self._token = make_secure_token()
        self.can_visit = can_visit
        self.can_edit = can_edit
        self.is_admin = is_admin
        self.must_reset_pw = must_reset_pw

        if errors:
            raise ValueError(*errors)

    @property
    def user_id(self):
        return self._id

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self._token

    def validate_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @classmethod
    def get(cls, _id):
        """
        Get a user by their id or name from the database.

        :param _id: the id (as an int) or name (as a str) of the user to get
        :return: the user object in question or :class:`None` if no user
            exists with the given id or name
        """
        if type(_id) is int:
            return cls.query.get(_id)
        elif type(_id) is str or type(_id) is unicode:
            return cls.query.filter(cls.name == _id).first()
        else:
            return None

    @classmethod
    def get_by_token(cls, token):
        """
        Get a user by their token from the database.

        :param token: The token of the user to get.
        :return: the user object in question or :class:`None` if no
            user exists with the token given
        """
        return User.query.filter(User._token == token).first()

    @classmethod
    def all(cls):
        """
        Get all users from the database.

        :return: a list of all users in the database
        """
        return cls.query.all()


@lm.user_loader
def load_(token):
    return User.get_by_token(token)


class Anonymous(AnonymousUserMixin):

    def __init__(self):
        pass

    @property
    def name(self):
        return _("Unknown")

    @property
    def user_id(self):
        return 0


lm.anonymous_user = Anonymous


def make_secure_token():
    """
    Generate a session token by which the user session will be identified. This
    is tied to the account and allows getting the account from a session cookie.

    :return: a random token
    """
    return pwgen(TOKEN_LENGTH, no_symbols=True)

# vim: set expandtab ts=4 sw=4:
