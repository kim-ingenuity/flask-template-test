import json
import os
from typing import Dict, Type

from dotenv import load_dotenv

from core.utils import convert_to_boolean, make_db_connection_url

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path='core/.env')


class Config(object):
    conn_url = make_db_connection_url(
        drivername=os.getenv('CONN_DRIVERNAME'),
        username=os.getenv('CONN_USERNAME'),
        password=os.getenv('CONN_PASSWORD'),
        host=os.getenv('CONN_HOST'),
        port=os.getenv('CONN_PORT'),
        database=os.getenv('CONN_DATABASE', ''),
        query=json.loads(os.getenv('CONN_QUERY', '{}'))
    )

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or conn_url.__to_string__(hide_password=False)
    SQLALCHEMY_TRACK_MODIFICATIONS = convert_to_boolean(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False))
    SQLALCHEMY_SESSION_NO_AUTOFLUSH = convert_to_boolean(os.getenv('SQLALCHEMY_SESSION_NO_AUTOFLUSH', False))
    
    DATABASE_SCHEMA = json.loads(os.getenv('DATABASE_SCHEMA', '{}'))
    FK_DATABASE_SCHEMA = f"{DATABASE_SCHEMA.get('schema')}." if DATABASE_SCHEMA.get('schema', '') else ''

    CCB_PREPAID_DB_SCHEMA = json.loads(os.getenv('CCB_PREPAID_DB_SCHEMA', '{}'))

    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    RESTPLUS_MASK_SWAGGER = convert_to_boolean(os.getenv('RESTPLUS_MASK_SWAGGER', False))
    DEFAULT_PAGINATION_SIZE = os.getenv('DEFAULT_PAGINATION_SIZE', 10)
    ERROR_404_HELP = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = convert_to_boolean(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True))


class ProductionConfig(Config):
    pass


config_by_name: Dict[str, Type[Config]] = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)
