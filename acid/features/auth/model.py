# -*- coding: utf-8 -*-
from acid.config import Config, config


class User:
    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email

    def is_admin(self):
        user_roles = Config(config['default']['users_file'])
        return self.email in user_roles['admins']
