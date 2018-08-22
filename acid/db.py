# -*- coding: utf-8 -*-
import os

from pony.orm import Database

from flask import current_app

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('DBPASSWORD'):
    raise Exception("On production use environment variables")

db = Database()


def connect():
    try:
        db.bind(provider=current_app.config['database']['provider'],
                host=os.getenv('DBHOST',
                               current_app.config['database']['host']),
                port=os.getenv('DBPORT',
                               current_app.config['database']['port']),
                user=os.getenv('DBUSER',
                               current_app.config['database']['user']),
                passwd=os.getenv('DBPASSWORD',
                                 current_app.config['database']['password']),
                db=os.getenv('DBNAME', current_app.config['database']['name']))
        db.generate_mapping()
    except TypeError:
        # Database object was already bound to provider
        pass
    return db
