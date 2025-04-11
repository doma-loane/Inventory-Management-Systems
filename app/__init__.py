from flask import Flask
from app.extensions import db
from app.routes import register_blueprints

def create_app(config_class="config.TestingConfig"):
    """Application factory for creating a Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register all blueprints
    register_blueprints(app)

    return app

# Optional: allow importing 'app' directly if needed
app = create_app()
