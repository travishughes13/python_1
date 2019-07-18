# This file sets up the main part of my server. It is where I pass information from other places to be rendered when the server is spun up and running

# Here, I am importing a specific rendering function (class?) that allows me to render my html template in the templates folder. It does this via the Jinga2 template engine
from flask import render_template, flash, redirect, request, url_for
#Now to pull in some URL parsing
from werkzeug.urls import url_parse
# Here, I'm importing my __init__.py file that sets up my basic server
from app import app
#Here, I'm going to import my LoginForm Class so that I can direct the server route to it
from app.forms import LoginForm
#Now I'm going to import the current_user and the login_user
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from app.models import User
from app import db
from app.forms import RegistrationForm

#I'm going to force login and handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Here, I'm declaring my variable routes and setting a placeholder for the user object
@app.route('/')
@app.route('/index')
@login_required
def index():
    # This defines the current user
    user = {'username':'Travis'}
    # This defines the posts that the user can see
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)