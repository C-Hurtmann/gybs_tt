from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger

from app.models import db
from app.routes import users_bp
from app.erros import register_error_handlers
from config import Config, DevConfig


def create_app(config: Config = DevConfig):
    app = Flask(__name__)
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, config=swagger_config)
    # Load onfig
    app.config.from_object(config)
    # Registrate blueprint
    app.register_blueprint(users_bp, url_prefix='/users')
    register_error_handlers(app)
    db.init_app(app)
    Migrate(app, db)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', port=5000)
