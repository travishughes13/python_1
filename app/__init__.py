#This imports Flask
from flask import Flask
#This imports my Config
from config import Config
#This imports the database instance
from flask_sqlalchemy import SQLAlchemy
#This import the database migration engine
from flask_migrate import Migrate
#This imports the Flask Login state manager
from flask_login import LoginManager
# importing my logging config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

#This creates my app variable
app = Flask(__name__)
#Now I'm passing app to the Login Manager
login = LoginManager(app)
#Here I require the user to login by directing them to the login page
login.login_view = 'login'
#Now I'm instantiating Config
app.config.from_object(Config)
#This is the database
db = SQLAlchemy(app)
#This is the migration engine
migrate = Migrate(app, db)
# This is for error reporting (via email)
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth=None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='noreply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

#This imports my routes
from app import routes, models, errors