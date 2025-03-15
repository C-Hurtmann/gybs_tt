from flask_migrate import Migrate
from flask import Flask

from app.models import db
from app.routes import users_bp
from app.erros import register_error_handlers
from config import Config


def create_app(config: Config):
    app = Flask(__name__)
    # Load onfig
    app.config.from_object(config)
    # Registrate blueprint
    app.register_blueprint(users_bp, url_prefix='/users')

    db.init_app(app)
    Migrate(app, db)
    register_error_handlers(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', port=5000)
