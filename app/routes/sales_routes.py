from flask import Blueprint

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/')
def sales_home():
    """Mocked sales home route for testing."""
    return "Sales Home"

@sales_bp.route('/sales')
def sales_dashboard():
    """Mocked sales dashboard route for testing."""
    return "Sales dashboard (mocked for testing)"
