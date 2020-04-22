from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from chatapp.src.models import User
import re


class MessageForm(FlaskForm):
    message = StringField("", validators=[DataRequired()])
    submit = SubmitField("Send")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def get_form(self):
        forms = [self.username, self.email, self.password, self.confirmPassword]
        return forms

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken!')
        if " " in username.data:
            raise ValidationError('Usernames cannot contain spaces!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken!')

    def validate_password(self, password):
        # secure password rege : ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.search(regex, password.data):
            raise ValidationError('Password must contain atleast one uppercase, one lowercase, one number, 8 char!')

class LoginForm(FlaskForm):
    username_email = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
