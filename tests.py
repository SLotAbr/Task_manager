import os
# The following line MUST be written BEFORE the db import. Otherwise the
# tests will run on the development/production database, so this
# program will drop all the existing tables after the first test
os.environ['DATABASE_URL'] = 'sqlite://' # an in-memory SQLite database

import requests
import unittest
from app import app, db
from app.models import User, Task


class UserModelCase(unittest.TestCase):
	def setUp(self):
		# makes application instance and its configuration data 
		# accessible to Flask extensions
		self.app_context = app.app_context()
		self.app_context.push()
		# creates all the database tables
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_base_models(self):
		u1 = User(username='abby', email='abby@example.com')
		u2 = User(username='john', email='john@example.com')
		u3 = User(username='bob', email='bob@example.com')
		db.session.add_all([u1, u2, u3])

		# the user instanse should be assigned to the 'executor' field 
		# (the 'backref' argument from the user model)
		# the 'executor_id' field from the task model keeps a different info
		t1 = Task(title='separate db',
			description='try not to drop your entire database',
			status='In progress', executor=u1)
		t2 = Task(title='db import',
			description='change the db_url for tests before the db import',
			status='completed', executor=u2)
		t3 = Task(title='user credentials',
			description='add any code to process the user credentials',
			status='Created', executor=u3)
		db.session.add_all([t1, t2, t3])
		db.session.commit()

		self.assertTrue(t1.executor == u1)
		self.assertTrue(t2.executor == u2)
		self.assertTrue(t3.executor == u3)

		self.assertEqual(u1.username, 'abby')
		self.assertEqual(u3.email, 'bob@example.com')

		t4 = Task(title='multiple tasks',
			description='check many-to-many relationship', 
			status='In progress', executor=u1)
		db.session.add(t4)
		db.session.commit()

		f = u1.tasks.all()
		self.assertEqual(f, [t1, t4])

	def test_API(self):
		# The app instance is created as a global variable and because of that 
		# the app API works with the original database. The way to fix it:
		# write a function that creates an application instance at runtime.
		url = 'http://localhost:5000/api/tokens'
		token = requests.post(url, auth=('test','test')).json()['token']
		# print(Task.query.all())
		auth_data = {'Authorization':f'Bearer {token}'}

		# errors for the 'create_task' view function
		# [ERROR] do not include title or executor_id fields in your request
		# [ERROR] use an incorrect executor_id
		# [ERROR] create a task twice
		# errors for the 'update_task' view function
		# [ERROR] do not include all of the following fields: 
		# 		['title', 'description', 'status', 'executor_id']
		# [ERROR] create a duplicate task

		# POST request
		data = {
			'title':'API testing',
			'description':'check the tests before a merge',
			'executor_id':1
		}
		response = requests.post(
			'http://localhost:5000/api/tasks', 
			headers=auth_data,
			json=data
		)
		task_id = response.json()['id']
		self.assertTrue(response.status_code == 201)

		# GET requests
		response = requests.get('http://localhost:5000/api/tasks', headers=auth_data)
		self.assertTrue(response.status_code == 200)

		response = requests.get('http://localhost:5000/api/tasks/2', headers=auth_data)
		self.assertTrue(response.status_code == 200)

		# PUT request
		data = {
			'title':'merge your repository branches',
			'status':'In progress'
		}
		response = requests.put(
			'http://localhost:5000/api/tasks/2', 
			headers=auth_data,
			json=data
		)
		self.assertTrue(response.status_code == 200)

		# DELETE request
		response = requests.delete('http://localhost:5000/api/tasks/2', headers=auth_data)
		self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
	unittest.main(verbosity=2)
