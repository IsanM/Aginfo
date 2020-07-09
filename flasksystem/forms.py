import self as self
from flask_wtf import FlaskForm, RecaptchaField
import email_validator
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flasksystem.models import User, Area, Devisionoffice
import phonenumbers
from flask_login import current_user


# Registration form
class RegistrationForm(FlaskForm):
    fristname = StringField('Frist Name', validators=[DataRequired(), Length(min=4, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10)])
    # district = SelectField('District', choices=[], validators=[DataRequired()], coerce=int)
    # area = SelectField('Area', choices=[], validators=[DataRequired()], coerce=int)
    # usertype = SelectField('User Type', choices=[('Farmer','Farmer')], validators=[DataRequired()]
    # devisionoffice = SelectField('Devison Office', choices=[], validators=[DataRequired()], coerce=int)
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.Please choose a another email!')

    def validate_phone(self, phone):

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That Phone Number is taken.Please choose a another Phone Number!')


# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login Here')


# Update Account Form Validations
class UpdateAccountForm(FlaskForm):
    fristname = StringField('Frist Name', validators=[DataRequired(), Length(min=4, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10)])
    # district = SelectField('District', choices=[], validators=[DataRequired()], coerce=int)
    # area = SelectField('Area', choices=[], validators=[DataRequired()], coerce=int)
    # active = SelectField('Account Status', choices=[('1', 'Active'), ('0', 'Deactive')], validators=[DataRequired()])
    # devisionoffice = SelectField('Devison Office', choices=[], validators=[DataRequired()],coerce=int)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update My Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.Please choose a another email!')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('That Phone Number is taken.Please choose a another Phone Number!')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request to password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email!,You must Register Frist')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class InsertNewFarmForm(FlaskForm):
    farmname = StringField('Farm Name', validators=[DataRequired(), Length(min=4, max=50)])
    latitude = IntegerField('Laitude', validators=[DataRequired()])
    longitude = IntegerField('Longtude', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])


