from config import Config
from flask import Flask, render_template
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
@app.route('/index')
def hello_world():
	return render_template('index.html')


@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', form=form)
