from datetime import datetime
from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='executor', lazy='dynamic')

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
