from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from werkzeug.http import HTTP_STATUS_CODES


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


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


@token_auth.verify_token
def verify_token(token):
	return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
	payload = {'error': HTTP_STATUS_CODES.get(status, 'Unknown error')}
	return payload, status
