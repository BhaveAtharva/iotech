from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired,  Length, EqualTo


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
    
    submit_button = SubmitField('signup')

class LoginForm(FlaskForm):
    username = StringField('username', 
        validators = [InputRequired(message = "put input"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])

    password = PasswordField('password',
        validators = [InputRequired(message = "password required"),
                        Length(min = 4, max = 25, message = "length between 4 to 25")])

    remember = BooleanField('remember me')