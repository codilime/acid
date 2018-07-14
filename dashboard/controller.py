# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

status = Blueprint('status', __name__, template_folder='templates')
builds = Blueprint('builds', __name__, template_folder='templates')


@status.route('/', methods=['GET'])
@status.route('/status', methods=['GET'])
def show_status():
    return render_template('status.html')


@builds.route('/builds', methods=['GET'])
def show_builds():
    return render_template('builds.html')
