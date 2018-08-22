# -*- coding: utf-8 -*-
from flask import current_app, session

from acid.settings_reader import read_yaml


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
        user_roles = read_yaml(current_app.config['default']['users_file'])
        return self.email in user_roles['admins']
