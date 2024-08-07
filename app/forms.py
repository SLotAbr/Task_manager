from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class TaskForm(FlaskForm):
	title = StringField('Title', 
		validators=[DataRequired(), Length(min=0, max=140)])
	description = TextAreaField('Description', 
		validators=[Length(min=0, max=2000)])
	executor = StringField('Executor username', 
		validators=[DataRequired(), Length(min=0, max=64)])
	submit = SubmitField('Submit')

	def validate_executor(self, executor):
		user = User.query.filter_by(username=executor.data).first()
		if user is None:
			raise ValidationError('User with the given username does not exist.')
