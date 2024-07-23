import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# A key for cryptographic purposes
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
