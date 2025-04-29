from flask import Flask
from .extensions import db, migrate
import logging
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Import all models to ensure they're registered
        from .models import Inventory, StockHistory, Sale, User
        
        # Log table names for verification
        logger.info(f"Registered tables: {db.metadata.tables.keys()}")
        
        # Create tables if they don't exist
        db.create_all()
    
    @app.shell_context_processor
    def make_shell_context():
        def list_tables():
            """List all tables in the database"""
            inspector = inspect(db.engine)
            return inspector.get_table_names()
            
        def verify_tables():
            """Verify table structures"""
            inspector = inspect(db.engine)
            tables_info = {}
            for table_name in inspector.get_table_names():
                tables_info[table_name] = {
                    'columns': [col['name'] for col in inspector.get_columns(table_name)],
                    'indexes': inspector.get_indexes(table_name)
                }
            return tables_info
            
        return dict(
            db=db,
            list_tables=list_tables,
            verify_tables=verify_tables,
            Inventory=Inventory,
            StockHistory=StockHistory,
            Sale=Sale,
            User=User
        )
    
    return app
