import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
# db.drop_all()
# db.create_all()


flask_bcrypt = Bcrypt(app)
migrate = Migrate(app, db, compare_type=True)


app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

from testingapp.routes.auth import auth_bp
from testingapp.routes.test import test_bp
from testingapp.routes.part import part_bp
from testingapp.routes.subject import subject_bp
from testingapp.routes.section import section_bp
from testingapp.routes.item import item_bp
from testingapp.routes.itemresult import item_result_bp
from testingapp.routes.option import option_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(test_bp, url_prefix='/api')
app.register_blueprint(part_bp, url_prefix='/api')
app.register_blueprint(section_bp, url_prefix='/api')
app.register_blueprint(subject_bp, url_prefix='/api')
app.register_blueprint(item_bp, url_prefix='/api')
app.register_blueprint(item_result_bp, url_prefix='/api')
app.register_blueprint(option_bp, url_prefix='/api')
