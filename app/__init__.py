from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app)

    # Register routes
    from app.routes import register_routes
    register_routes(app)

    # Make app accessible for testing
    return app

# Optional: allow importing 'app' directly if needed
app = create_app()
