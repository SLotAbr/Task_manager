from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# simplifies further updates to the database structure 
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # the function name from app/routes.py


from app import routes, models
