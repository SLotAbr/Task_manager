from base64 import b64encode
from datetime import datetime, timedelta
from os import urandom
from time import time
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
import jwt


# the UserMixin class includes implementation of the following methods:
# is_authenticated, is_active, is_anonymous, get_id
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='executor', lazy='dynamic')
	token = db.Column(db.String(32), index=True, unique=True)
	token_expiration = db.Column(db.DateTime)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def get_reset_password_token(self, expires_in=600):
		# The contents of the jwt token can be decoded easily by anyone. Yet 
		# the payload is signed and protected from tampering: you cannot change
		# its contents without invalidating it. JWT (RFC7519) is just a compact
		# way to safely transmit claims from an issuer to the audience over HTTP.
		# If you want to encrypt the content (make it visible only to issuer and 
		# the consumer), there is JWE standard for that (jose, jwcrypto)
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			# The token cannot be validated or is expired: returns 'None'
			return
		return User.query.get(id)

	# this tokens is used for API authentication purposes
	def get_token(self, expires_in=3600):
		now = datetime.utcnow()
		if self.token and self.token_expiration > now + timedelta(seconds=60):
			return self.token
		self.token = b64encode(urandom(32)).decode('utf-8')
		self.token_expiration = now + timedelta(seconds=expires_in)
		db.session.add(self)
		return self.token

	def revoke_token(self):
		self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

	@staticmethod
	def check_token(token):
		user = User.query.filter_by(token=token).first()
		if user is None or user.token_expiration < datetime.utcnow():
			return None
		return user


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	description = db.Column(db.String(2000))
	created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# Is there any better db.type to store the status values?
	status = db.Column(db.String(11), index=True, default='Created')
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Task {}>'.format(self.title)

	def to_dict(self):
		data = {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
			'status': self.status,
			'executor_id': self.executor_id,
			'self': url_for('api.get_task', id=self.id),
		}
		return data

	def from_dict(self, data):
		# the client can change only the following fields
		for field in ['title', 'description', 'status', 'executor_id']:
			if field in data:
				self.updated_at = datetime.utcnow()
				setattr(self, field, data[field])


# connects Flask's user session with the user representation in the database
# Flask-login requires you to define this function
@login.user_loader
def load_user(id):
	return User.query.get(int(id))
