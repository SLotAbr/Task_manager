from flask import render_template, redirect
from app import app
from app.forms import LoginForm


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
