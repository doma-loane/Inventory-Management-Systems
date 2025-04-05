from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from celery import Celery

db = SQLAlchemy()  # Initialize db here
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
celery = Celery()
