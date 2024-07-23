from config import Config
from flask import Flask, render_template, redirect
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# simplifies further updates to the database structure 
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def hello_world():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# redirects the user if the submit is successful
	if form.validate_on_submit():
		# TODO: process the user credentials
		return redirect('/index')
	return render_template('login.html', form=form)
