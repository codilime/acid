# -*- coding: utf-8 -*-
import os

from pony.orm import Database

from dashboard.config import config

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('DBPASSWORD'):
    raise Exception("On production use environment variables")

db = Database()


def connect():
    try:
        db.bind(provider=config['DATABASE']['provider'],
                host=os.getenv('DBHOST', config['DATABASE']['host']),
                user=os.getenv('DBUSER', config['DATABASE']['user']),
                passwd=os.getenv('DBPASSWORD', config['DATABASE']['password']),
                db=os.getenv('DBNAME', config['DATABASE']['name']))
        db.generate_mapping()
    except TypeError:
        # Database object was already bound to provider
        pass
    return db
