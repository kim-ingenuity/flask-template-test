from app.api import blueprint
from core.main import create_app


app = create_app('prod')
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
