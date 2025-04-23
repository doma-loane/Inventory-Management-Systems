from flask import Blueprint, request, jsonify
from app import db
from app.models import Inventory

bp = Blueprint('inventory', __name__, url_prefix='/api')

@bp.route('/add_product', methods=['POST'])
def add_product():
    """Add a product to the inventory."""
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'stock' not in data:
        return jsonify({"message": "Invalid data"}), 400

    product = Inventory(
        item_name=data['name'],
        unit_price=data['price'],
        total_stock=data['stock'],
        category=data.get('category', 'Uncategorized'),
        product_code=data.get('product_code', '000000')
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added", "id": product.id}), 201

@bp.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    # Simulate updating stock in the database
    return jsonify({'message': 'Stock updated'}), 200

@bp.route('/', strict_slashes=False)
def get_inventory():
    return jsonify([{"id": 1, "name": "Test Product", "stock": 100}]), 200

@bp.route('/home')
def home():
    return "Inventory Home"
