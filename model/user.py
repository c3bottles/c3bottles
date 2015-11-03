from c3bottles import lm

class User():

    def __init__(self, name, can_visit=False, can_edit=False):
        self.name = name
        self.can_visit = can_visit
        self.can_edit = can_edit

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.name)

users = {
    "collector": User("collector", can_visit=True, can_edit=False),
    "master": User("master", can_visit=True, can_edit=False)
}

@lm.user_loader
def load_user(user_id):
    return users[user_id]



# vim: set expandtab ts=4 sw=4:
