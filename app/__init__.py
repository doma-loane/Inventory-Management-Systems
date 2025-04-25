from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes import register_all_blueprints

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object("config")  # Load configuration from config.py

    # Debugging: Print the database URI and other key configurations
    print("Loaded Configuration:")
    print("SQLALCHEMY_DATABASE_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("DEBUG:", app.config.get("DEBUG"))
    print("TESTING:", app.config.get("TESTING"))

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate for database migrations

    # Register blueprints
    register_all_blueprints(app)

    return app

# Create the global application object
app = create_app()
