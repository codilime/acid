# -*- coding: utf-8 -*-
from dashboard.config import Config, config


def is_admin(email):
    user_roles = Config(config['default']['users_file'])
    return email in user_roles['admins']
