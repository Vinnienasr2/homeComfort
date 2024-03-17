# app.py

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy
from models import User, create_super_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, app
from admin import admin, ModelView


# Define Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Sign Up')

# Define Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')


class HomeForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')

# Routes
@app.route("/")
def home():
    if 'username' not in session:
        flash('Please log in to access the home page.', 'info')
        return redirect(url_for('login'))

    form = HomeForm()
    return render_template('home.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    db.create_all()
    with app.app_context():
        create_super_user()

    admin.add_view(ModelView(User, db.session))
    
    app.run(debug=True)

