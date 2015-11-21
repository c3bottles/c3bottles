from werkzeug.security import check_password_hash

from controller import lm

class User():

    def __init__(self, user_id):
        if user_id in users:
            self._id = user_id
            self._name = users[user_id]["name"]
            self._can_visit = users[user_id]["can_visit"]
            self._can_edit = users[user_id]["can_edit"]
            self._password = users[user_id]["pw"]
        else:
            raise ValueError("User not found.")

    def get_id(self):
        return self._id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def can_visit(self):
        return self._can_visit

    @property
    def can_edit(self):
        return self._can_edit

    def validate_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def name(self):
        return self._name

    @classmethod
    def get(cls, user_id):
        try:
            return cls(user_id)
        except ValueError:
            return None

users = {
    "collector": {
        "can_visit": True,
        "can_edit": False,
        "name": "Bottle Collector",
        "pw": "pbkdf2:sha1:1000$eYZPJm1o$10fea6fce2e9a51dd1f6add59adc964fa17af22f" # "changeme"
    },
    "master": {
        "can_visit": True,
        "can_edit": True,
        "name": "Bottle Master",
        "pw": "pbkdf2:sha1:1000$eYZPJm1o$10fea6fce2e9a51dd1f6add59adc964fa17af22f" # "changeme"
    }
}

@lm.user_loader
def load_user(user_id):
    return User.get(user_id)

# vim: set expandtab ts=4 sw=4:
