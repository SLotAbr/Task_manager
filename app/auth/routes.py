from flask import render_template, redirect, url_for, flash
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
	ResetPasswordForm
from app.models import User
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	# redirects the user if the submit is successful
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your registration is successful!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		# The message is displayed even if the provided email is unknown. 
		# This way clients cannot use the form to figure out if a 
		# given user is a member or not
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html',
							title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)
