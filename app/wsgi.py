import logging

from app.api import blueprint
from core.main import create_app


app = create_app('prod')
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run()

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
