from flask import request, url_for
from app import db
from app.api import bp
from app.models import User, Task


@bp.route('/tasks', methods=['POST'])
def create_task():
	data = request.get_json() or {}
	if ('title' not in data) or ('executor_id' not in data):
		payload = {'error':'Bad Request'}
		payload['message'] = 'your request must include title and executor_id fields'
		return payload, 400
	User.query.get_or_404(data['executor_id'])
	is_existed = Task.query.filter_by(
		title=data['title'], 
		description=data['description'] if 'description' in data else '',
		executor_id=data['executor_id']
	).first()
	if is_existed:
		payload = {'error':'Conflict'}
		payload['message'] = 'A task with given fields already exists. '\
			f'Its id: {is_existed.id}. You can use the "PUT" method to update it'
		return payload, 409
	else:
		# 'title', 'executor_id' are in data; 
		# an executor with this id is existing;
		# the data content is original
		task = Task()
		data['status'] = 'Created'
		task.from_dict(data)
		db.session.add(task)
		db.session.commit()
	# This status code means that a new entity has been created. Besides, the
	# HTTP protocol requires that a 201 response includes a `Location` header
	# that is set to the URL of the new resource
	return task.to_dict(), 201, {'Location': url_for('api.get_task', id=task.id)}


@bp.route('/tasks', methods=['GET'])
def get_tasks():
	tasks = Task.query.all()
	return { 'items': [item.to_dict() for item in tasks] }


@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
	return Task.query.get_or_404(id).to_dict()


@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
	pass


@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
	pass
