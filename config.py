import os

class Config:
    """Base configuration class for the inventory system."""
    
    # Security Key
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

    # Database Configuration (Supports Multiple Databases)
    DB_TYPE = os.environ.get("DB_TYPE", "sqlite")  # Options: sqlite, postgresql, mysql
    if DB_TYPE == "sqlite":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///inventory.db")
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
