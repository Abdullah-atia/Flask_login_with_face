from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField(label='User Name ', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password ', validators=[Length(min=8, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm Password ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self, check_new_username):
        user = User.query.filter_by(username=check_new_username.data).first()
        if user:
            raise ValidationError('Username already used, Please try to use onther one!')

    def validate_email_address(self, check_new_email):
        email_address = User.query.filter_by(email_address=check_new_email.data).first()
        if email_address:
            raise ValidationError('Email already used, Please try to use onther one!')
    
class LoginForm(FlaskForm):
    username = StringField(label='User Name ', validators=[DataRequired()])
    password = PasswordField(label='Password ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class TakeForm(FlaskForm):
    submit = SubmitField(label='save')
