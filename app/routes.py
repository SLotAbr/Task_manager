from flask import render_template
from app import app
from app.models import Task
from flask_login import login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')


@app.route('/users')
@login_required
def users():
	return render_template('users.html')


@app.route('/tasks')
@login_required
def tasks():
	return render_template('tasks.html')
