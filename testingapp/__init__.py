from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

import os

flask_bcrypt = Bcrypt()


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
flask_bcrypt.init_app(app)
migrate = Migrate(app, db)

from testingapp.routes import auth