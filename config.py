import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# A key for cryptographic purposes
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	# https://docs.python.org/2/library/logging.handlers.html#smtphandler
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['test@example.com']
