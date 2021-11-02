import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
#db.drop_all()
#db.create_all()


flask_bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

from testingapp.routes.auth import auth_bp
from testingapp.routes.test import test_bp
from testingapp.routes.subject import subject_bp


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(test_bp, url_prefix='/api')
app.register_blueprint(subject_bp, url_prefix='/api')
