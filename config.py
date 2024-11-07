from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('db_user')}:{config('db_pass')}"
        f"@{config('db_host')}:{config('db_port')}/{config('db_name')}"
    )


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('db_user')}:{config('db_pass')}"
        f"@{config('db_host')}:{config('db_port')}/{config('db_name')}"
    )


class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('db_user')}:{config('db_pass')}"
        f"@{config('db_host')}:{config('db_port')}/{config('test_db_name')}"
    )


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environment)

    db.init_app(app)
    Migrate(app, db)
    api = Api(app)
    [api.add_resource(*route) for route in routes]
    return app
