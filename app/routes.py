from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import TaskForm, EditTaskForm
from app.models import User, Task
from flask_login import login_required
from datetime import datetime


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


@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
	form = EditTaskForm()
	current_task = Task.query.filter_by(id=task_id).first_or_404()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.executor.data).first()
		task = Task.query.filter_by(
			title=form.title.data, 
			description=form.description.data, 
			executor=user
		).first()
		if task is not None:
			if task.id != task_id:
				flash(f'This task already exists. Its id: {task.id}.')	
		else:
			current_task.title = form.title.data
			current_task.description = form.description.data
			current_task.status = form.status.data
			current_task.executor = user
			current_task.updated_at = datetime.utcnow()
			db.session.commit()
			flash('Your changes have been saved.')
		return redirect(url_for('edit_task', task_id=task_id))
	elif request.method == 'GET':
		form.title.data = current_task.title
		form.description.data = current_task.description
		form.status.data = current_task.status
		form.executor.data = current_task.executor.username
	return render_template('edit_task.html', form=form)
