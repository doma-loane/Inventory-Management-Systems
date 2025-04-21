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

def register_blueprints(app):
    from .inventory_routes import inventory_bp
    from .sales_routes import sales_bp

    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(sales_bp, url_prefix="/sales")

def register_all_blueprints(app):
    from .inventory_routes import bp as inventory_bp
    from .product_routes import bp as product_bp
    from .auth_routes import bp as auth_bp

    app.register_blueprint(inventory_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)

__all__ = ['register_blueprints']  # Ensure it's importable

all_blueprints = [inventory_bp, auth_bp, sales_bp]  # Ensure sales_bp is included
