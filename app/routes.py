from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import TaskForm
from app.models import User, Task
from flask_login import login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = TaskForm()
	# redirects the user if the submit is successful
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.executor.data).first()
		task = Task(title=form.title.data, 
			description=form.description.data, executor=user)
		db.session.add(task)
		db.session.commit()
		flash('Your task is now live!')
		# the `Post/Redirect/Get` pattern
		return redirect(url_for('tasks'))
	return render_template('index.html', form=form)


@app.route('/users')
@login_required
def users():
	users = User.query.all()
	return render_template('users.html', users=users)


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	tasks = user.tasks.order_by(Task.created_at.desc()).all()
	return render_template('user.html', user=user, tasks=tasks)


@app.route('/tasks')
@login_required
def tasks():
	tasks = Task.query.order_by(Task.created_at.desc()).all()
	return render_template('tasks.html', tasks=tasks)


@app.route('/task/<task_id>')
@login_required
def task(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	return render_template('task.html', task=task)
