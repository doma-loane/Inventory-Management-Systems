# All Flask Routes (Views)
from .auth import auth_bp
from .inventory import inventory_bp
from .sales import sales_bp

def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    from app.routes.inventory_routes import inventory_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")

# Ensure routes are not removed
