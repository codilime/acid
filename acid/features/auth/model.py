# -*- coding: utf-8 -*-
from flask import session

from acid.config import Config, config


def get_current_user():
    if not session:
        return None
    else:
        return session.get('user')


class User:
    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email

    def is_admin(self):
        user_roles = Config(config['default']['users_file'])
        return self.email in user_roles['admins']
