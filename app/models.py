from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# the UserMixin class includes implementation of the following methods:
# is_authenticated, is_active, is_anonymous, get_id
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='executor', lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)


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


# connects Flask's user session with the user representation in the database
# Flask-login requires you to define this function
@login.user_loader
def load_user(id):
	return User.query.get(int(id))
