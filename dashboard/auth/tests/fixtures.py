# -*- coding: utf-8 -*-

from dashboard.auth.model import User


class UserFactory:
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    @staticmethod
    def get_user(role):
        if role == UserFactory.ROLE_ADMIN:
            attrs = {'full_name': 'Admin Admin',
                     'email': 'admin@acid.test'}
        else:
            attrs = {'full_name': 'Noname Guest',
                     'email': 'noname@guest.test'}
        return User(**attrs)
