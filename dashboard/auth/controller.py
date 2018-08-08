import requests
from flask import url_for, Blueprint, current_app, make_response, render_template
from werkzeug.utils import redirect

from dashboard.auth import service
from dashboard.controller import error_handlers
from dashboard.auth.exceptions import AuthenticationFailed

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/sign_in')
def sign_in():
    redirect_url = service.start_openid_auth()
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


@error_handlers.app_errorhandler(AuthenticationFailed)
def auth_error(error):
    current_app.logger.error(f'{error}; raised on URL: {request.url}')
    return make_response(render_template('auth_error.html'),
                         requests.codes.unauthorized)
