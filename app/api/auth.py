from flask_httpauth import HTTPBasicAuth
from app.models import User
from werkzeug.http import HTTP_STATUS_CODES


basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
	user = User.query.filter_by(username=username).first()
	if user and user.check_password(password):
		# The authenticated user can be called by 'basic_auth.current_user()'
		return user


@basic_auth.error_handler
def basic_auth_error(status):
	# HTTP_STATUS_CODES provides a short descriptive name for each HTTP status code
	payload = {'error': HTTP_STATUS_CODES.get(status, 'Unknown error')}
	return payload, status
