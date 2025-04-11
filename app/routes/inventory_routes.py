from flask import Blueprint, request, jsonify
from app import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    # Simulate adding a product to the database
    return jsonify({'message': 'Product added', 'id': 1}), 201

@inventory_bp.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    # Simulate updating stock in the database
    return jsonify({'message': 'Stock updated'}), 200

@inventory_bp.route('/', strict_slashes=False)
def get_inventory():
    return jsonify([{"id": 1, "name": "Test Product", "stock": 100}]), 200
