from flask import Flask, url_for
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from core.settings import Config, config_by_name

db = SQLAlchemy(session_options={'autoflush': Config.SQLALCHEMY_SESSION_NO_AUTOFLUSH})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    return app


class PatchedApi(Api):
    """Overriden Flask API class to fix Swagger JSON documentation access"""
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        """
        return url_for(self.endpoint('specs'), _external=False)
