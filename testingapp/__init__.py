from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

import os

flask_bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate = Migrate(app, db)

    return app