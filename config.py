import os


class Config(object):
	# A key for cryptographic purposes
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
