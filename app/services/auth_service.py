import jwt
from datetime import datetime, timedelta
from flask import jsonify
from config import Config  # Use absolute import
from ..extensions import db  # Keep this if extensions.py is inside the same package

# Use the Config class directly to access configuration values
config = Config()

def generate_token(user):
    """
    Generate a JWT token for the authenticated user.
    :param user: User object
    :return: JWT token
    """
    try:
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate token"}), 500

def get_database_uri():
    """
    Retrieve the database URI from the configuration.
    """
    db_uri = config.SQLALCHEMY_DATABASE_URI
    return db_uri
