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

#This imports my routes
from app import routes, models