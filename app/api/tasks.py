from app.api import bp
from app.models import Task


@bp.route('/tasks', methods=['POST'])
def create_task():
	pass


@bp.route('/tasks', methods=['GET'])
def get_tasks():
	pass


@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
	return Task.query.get_or_404(id).to_dict()


@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
	pass


@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
	pass
