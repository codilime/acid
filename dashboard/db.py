# -*- coding: utf-8 -*-
import os

from pony.orm import Database

from dashboard.config import config

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('DBPASSWORD'):
    raise Exception("On production use environment variables")

db = Database()


def connect():
    try:
        db.bind(provider=config['database']['provider'],
                host=os.getenv('DBHOST', config['database']['host']),
                user=os.getenv('DBUSER', config['database']['user']),
                passwd=os.getenv('DBPASSWORD', config['database']['password']),
                db=os.getenv('DBNAME', config['database']['name']))
        db.generate_mapping()
    except TypeError:
        # Database object was already bound to provider
        pass
    return db
