# All Flask Routes (Views)
from .auth import auth_bp
from .inventory import inventory_bp
from .sales import sales_bp

def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(sales_bp, url_prefix="/sales")

# Ensure routes are not removed
