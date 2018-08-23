# -*- coding: utf-8 -*-
import os

from pony.orm import Database

from flask import current_app

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('DBPASSWORD'):
    raise Exception("On production use environment variables")

db = Database()


def connect():
    config = current_app.config['database']
    try:
        db.bind(provider=config['provider'],
                host=os.getenv('DBHOST', config['host']),
                port=os.getenv('DBPORT', config['port']),
                user=os.getenv('DBUSER', config['user']),
                passwd=os.getenv('DBPASSWORD', config['password']),
                db=os.getenv('DBNAME', config['name']))
        db.generate_mapping()
    except TypeError:
        # Database object was already bound to provider
        pass
    return db
