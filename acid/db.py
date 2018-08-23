# -*- coding: utf-8 -*-
import os

from pony.orm import Database

from flask import current_app

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('DBPASSWORD'):
    raise Exception("On production use environment variables")

db = Database()


def connect():
    config = current_app.config
    try:
        db.bind(provider=config['database']['provider'],
                host=os.getenv('DBHOST', config['database']['host']),
                port=os.getenv('DBPORT', config['database']['port']),
                user=os.getenv('DBUSER', config['database']['user']),
                passwd=os.getenv('DBPASSWORD', config['database']['password']),
                db=os.getenv('DBNAME', config['database']['name']))
        db.generate_mapping()
    except TypeError:
        # Database object was already bound to provider
        pass
    return db
