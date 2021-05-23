from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Email, ValidationError
from iotech.models import User

class RegistrationForm(FlaskForm):
    username = StringField('username', 
        validators = [InputRequired(message = "put input"),
                        # EqualTo(User.query.filter('username').first(), message = 'username already exists'),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])
    
    password = PasswordField('password',
        validators = [InputRequired(message = "password required"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])
    
    confirm_password = PasswordField('password1',
        validators = [EqualTo('password', message="passwords do not match"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])

    email = StringField('email', 
        validators = [InputRequired(), Email(message="Invalid email"), Length(max=100)])
    
    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('already registered using this email')



class LoginForm(FlaskForm):
    username = StringField('username', 
        validators = [InputRequired(message = "put input"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])

    password = PasswordField('password',
        validators = [InputRequired(message = "password required"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])
    
    remember = BooleanField('remember me')
        
    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if not user:
            raise ValidationError('Username does not exist')