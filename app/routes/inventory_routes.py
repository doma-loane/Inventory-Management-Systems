from flask import Blueprint, request, jsonify
from app import db

bp = Blueprint('inventory', __name__, url_prefix='/inventory')  # Added url_prefix for consistency

@bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    # Simulate adding a product to the database
    return jsonify({'message': 'Product added', 'id': 1}), 201

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
