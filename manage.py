import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.api import blueprint
from core.main import create_app, db
from core.settings import config_by_name, Config
from core.utils import ColoredPrint

clr_print = ColoredPrint()


def make_app(config_name=None):
    if config_by_name.get(config_name, None):
        app = create_app(config_name)
    else:
        app = create_app(os.getenv('FLASK_ENV') or 'prod')

    app.register_blueprint(blueprint)
    app.app_context().push()
    return app


manager = Manager(make_app)

manager.add_option(
    '-c',
    '--config_name',
    dest='config_name',
    help='Configuration to use. Available options: dev, prod',
    required=False,
)

@manager.option('-c', '--config', dest='config_name', default='dev', help='Configuration to use. Available options: dev, prod')
def create_tables(config_name='dev'):
    try:
        app = create_app(config_name)
        app.register_blueprint(blueprint)
        app.app_context().push()
        db.configure_mappers()

        db.create_all()
        clr_print.success('Successfully created tables on the database.')
    except Exception as err:
        clr_print.failed(f'Error creating tables due to {err}')


@manager.option('-c', '--config', dest='config_name', default='dev', help='Configuration to use. Available options: dev, prod')
def drop_tables(config_name='dev'):
    try:
        app = create_app(config_name)
        app.register_blueprint(blueprint)
        app.app_context().push()
        db.drop_all()
        clr_print.success('Successfully dropped tables from the database.')
    except Exception as err:
        clr_print.failed(f'Error dropping tables due to {err}')


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
