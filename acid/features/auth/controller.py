# -*- coding: utf-8 -*-
import requests

from flask import Blueprint, current_app, redirect, url_for

from acid.controller import error_handlers
from acid.error_handler import ErrorHandler, bind_error_handlers

from . import service
from .exceptions import AuthenticationFailed

auth = Blueprint('auth', __name__, template_folder='../../templates')


@auth.route('/sign_in')
def sign_in():
    config = current_app.config['core']['authentication']
    redirect_url = service.start_openid_auth(
        config['openid_providers']['launchpad']['url'])
    return redirect(redirect_url)


@auth.route('/signed_in')
def signed_in():
    user = service.fetch_user_data()
    service.create_user_session(user)
    return redirect(url_for('status.show_dashboard'))


@auth.route('/sign_out')
def sign_out():
    service.drop_user_session()
    return redirect(url_for('status.show_dashboard'))


handlers = [
    ErrorHandler([AuthenticationFailed], 'auth_error.html',
                 requests.codes.unauthorized)
]

bind_error_handlers(error_handlers, handlers)
