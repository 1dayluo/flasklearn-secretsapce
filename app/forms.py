from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError,Length,optional
from flask_wtf.file import FileRequired, FileAllowed
from app.operation import *

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    date = StringField()
    author = StringField('author')
    content = TextAreaField(validators=[DataRequired()])
    commit = SubmitField('submit')

class UploadAvatar(FlaskForm):
    avatar = FileField('avatar',validators=[FileRequired('文件未选择'), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    avatar = FileField('avatar',validators=[optional(),FileAllowed(['jpg', 'png'], 'Images only!')])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class ReplyForm(FlaskForm):
    reply = TextAreaField('reply', validators=[DataRequired()])
    submit = SubmitField('submit')