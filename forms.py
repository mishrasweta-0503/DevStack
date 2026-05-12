from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, SelectField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=2, max=20)])
    email = StringField('Email Address', validators = [validators.DataRequired(),validators.Length(min=6, max=35)])
    password = PasswordField('New Password', validators = [validators.DataRequired(),validators.Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm Password',validators = [validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators = [validators.DataRequired(),validators.Length(min=6, max=15)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = SubmitField('Login')

class ResourceForm(FlaskForm):
    title = StringField('Title', validators = [validators.DataRequired()])
    description = TextAreaField('Description')
    url = StringField('URL', validators=[validators.DataRequired()])
    category = SelectField('Choose Field', choices=[
            'Frontend', 'Backend', 'Database', 'Mobile', 
            'Web', 'Security', 'Full Stack'
        ])
    submit = SubmitField('Add Resource')