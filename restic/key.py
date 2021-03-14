from datetime import datetime


class Key(object):
    repo = None
    key_current = False
    key_id = None
    key_user = None
    key_host = None
    key_created = None

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def __str__(self):
        return f'{self.key_id},{self.key_user},{self.key_host},{self.key_created}'

    def is_valid(self):
        return self.repo is not None

    def check_valid(self):
        if not self.is_valid():
            raise RuntimeError(
                'The key is removed or updated, please get object from repo again'
            )

    def set_attr(self, attr, value):
        if attr.strip() == 'ID':
            self.key_id = value
        elif attr.strip() == 'User':
            self.key_user = value
        elif attr.strip() == 'Host':
            self.key_host = value
        elif attr.strip() == 'Created':
            if type(value) == datetime:
                self.key_created = value
            elif type(value) == str:
                self.key_created = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    # TODO: set methods type check
    def set_id(self, value):
        self.key_id = value

    def set_user(self, value):
        self.key_user = value

    def set_host(self, value):
        self.key_host = value

    def set_created(self, value):
        if type(value) == datetime:
            self.key_created = value
        elif type(value) == str:
            self.key_created = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def set_current(self, value):
        self.key_current = value

    def get_id(self):
        return self.key_id

    def get_user(self):
        return self.key_user

    def get_host(self):
        return self.key_host

    def get_created(self):
        return self.key_created

    def get_current(self, value):
        return self.key_current
