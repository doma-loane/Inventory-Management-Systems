# All Flask Routes (Views)
from .auth import auth_bp
from .inventory import inventory_bp
from .sales import sales_bp
# from .routes import main_blueprint  # Removed as it could not be resolved

def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    from .inventory_routes import inventory_bp
    from .auth_routes import auth_bp
    from .sales_routes import sales_bp

    # Register inventory, auth, and sales blueprints
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
