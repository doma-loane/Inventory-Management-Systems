from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')  # Default fallback

    # Load from .env as override
    load_dotenv()
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import inventory_routes, sales_routes
    app.register_blueprint(inventory_routes.bp)
    app.register_blueprint(sales_routes.bp)

    return app

# Optional: allow importing 'app' directly if needed
app = create_app()
