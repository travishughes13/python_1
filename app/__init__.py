#This imports Flask
from flask import Flask
#This imports my Config
from config import Config
#This imports the database instance
from flask_sqlalchemy import SQLAlchemy
#This import the database migration engine
from flask_migrate import Migrate

#This creates my app variable
app = Flask(__name__)
#Now I'm instantiating Config
app.config.from_object(Config)
#This is the database
db = SQLAlchemy(app)
#This is the migration engine
migrate = Migrate(app, db)

#This imports my routes
from app import routes, models