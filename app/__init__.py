from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.routes import register_all_blueprints

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    # ✅ Load testing environment if available
    if os.path.exists('.env.testing'):
        load_dotenv('.env.testing')
    else:
        load_dotenv()  # fallback to default .env

    app = Flask(__name__)

    # ✅ Set config based on FLASK_ENV
    env = os.getenv('FLASK_ENV')
    if env == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config import Config
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register all blueprints
    register_all_blueprints(app)

    return app

# Optional: allow importing 'app' directly if needed
app = create_app()
