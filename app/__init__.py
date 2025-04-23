from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.routes import register_all_blueprints

db = SQLAlchemy()  # Singleton SQLAlchemy instance
migrate = Migrate()

def create_app(config_name=None):
    # Load environment variables
    if os.path.exists('.env.testing'):
        load_dotenv('.env.testing')
    else:
        load_dotenv()

    app = Flask(__name__)

    # Set configuration
    if config_name:
        app.config.from_object(config_name)
    else:
        env = os.getenv('FLASK_ENV')
        if env == 'testing':
            from app.config import TestingConfig
            app.config.from_object(TestingConfig)
        else:
            from app.config import Config
            app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)  # Reuse the singleton db instance
    migrate.init_app(app, db)

    # Register blueprints
    register_all_blueprints(app)

    return app

# Optional: allow importing 'app' directly if needed
app = create_app()
