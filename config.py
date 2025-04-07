import os

class Config:
    """Base configuration class for the inventory system."""
    
    # Security Key
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

    # Database Configuration (Supports Multiple Databases)
    DB_TYPE = os.environ.get("DB_TYPE", "sqlite")  # Options: sqlite, postgresql, mysql
    if DB_TYPE == "sqlite":
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    elif DB_TYPE == "postgresql":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/inventory_db")
    elif DB_TYPE == "mysql":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql://user:password@localhost/inventory_db")
    else:
        raise ValueError("Invalid database type specified!")

    # Disable modification tracking to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload Folder for Images
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "static/uploads")

    # Barcode Scanner Configuration
    BARCODE_SCANNER_ENABLED = os.environ.get("BARCODE_SCANNER_ENABLED", "True").lower() in ("true", "1")

    # Debug Mode
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")

    # JWT Secret Key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")

    # Cache Configuration
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
