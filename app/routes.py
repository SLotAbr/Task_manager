from flask import render_template
from app import app
from app.models import User, Task
from flask_login import login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')


@app.route('/users')
@login_required
def users():
	users = User.query.all()
	return render_template('users.html', users=users)


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)


@app.route('/tasks')
@login_required
def tasks():
	tasks = Task.query.all()
	return render_template('tasks.html', tasks=tasks)
