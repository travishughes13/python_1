# This file sets up the main part of my server. It is where I pass information from other places to be rendered when the server is spun up and running

# Here, I am importing a specific rendering function (class?) that allows me to render my html template in the templates folder. It does this via the Jinga2 template engine
from flask import render_template, flash, redirect
# Here, I'm importing my __init__.py file that sets up my basic server
from app import app
#Here, I'm going to import my LoginForm Class so that I can direct the server route to it
from app.forms import LoginForm
#Now I'm going to import the current_user and the login_user
from flask_login import current_user, login_user
from app.models import User

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# Here, I'm declaring my variable routes and setting a placeholder for the user object
@app.route('/')
@app.route('/index')
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
    return render_template('index.html', title='Home', user=user, posts=posts)
