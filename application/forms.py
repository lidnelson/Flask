from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from application import bcrypt
from flask_login import current_user

class PostForm(FlaskForm):
	title = StringField('Title',
		validators=[
			DataRequired(),
			Length(min=4, max=100)
		])
	content = StringField('Content',
		validators=[
			DataRequired(),
			Length(min=50, max=10000)
		])
	submit = SubmitField('Post Content')




class RegistrationForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=2, max=100)
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=2, max=100)
		])
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	password = PasswordField('Password',
		validators=[
			DataRequired(),
			Length(min=4)
		])
	confirm_password = PasswordField('Confirm Password',
		validators=[
			DataRequired(),
			EqualTo('password')
		])
	submit =SubmitField('Sign Up')

	def validate_email(self,email):
		user =Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already in use!')





class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	password = PasswordField('Password',
		validators=[
			DataRequired()
		])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		user=Users.query.filter_by(email=self.email.data).first()
		if not user:
			raise ValidationError('Unknown email')
	
	def validate_password(self, password):
		user=Users.query.filter_by(email=self.email.data).first()
		if user: 
			if not bcrypt.check_password_hash(user.password,self.password.data):
				raise ValidationError('Invalid password')
			

class UpdateAccountForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=2, max=100)
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=2, max=100)
		])
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	submit = SubmitField('Update')

	def validate_email(self,email):
		if email.data != current_user.email:	
			user =Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use - Please choose another')
