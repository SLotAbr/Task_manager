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
# this view function will be used to protect routes with the 'login_required' 
# decorator from unauthenticated users
login.login_view = 'login'


from app import routes, models
