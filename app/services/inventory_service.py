import logging
from ..models.inventory import Inventory
from ..extensions import db
from flask import jsonify

def get_inventory_service(page, per_page):
    try:
        pagination = Inventory.query.paginate(page=page, per_page=per_page, error_out=False)
        inventory_data = [{
            "id": item.id,
            "name": item.item_name,
            "category": item.category,
            "subcategory": item.subcategory,
            "product_code": item.product_code,
            "unit_price": item.unit_price,
            "total_stock": item.total_stock
        } for item in pagination.items]
        return jsonify({
            "products": inventory_data,
            "page": pagination.page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }), 200
    except Exception as e:
        logging.error(f"Error fetching inventory: {e}")
        return jsonify({"error": "Failed to fetch inventory"}), 500

def add_product_service(data):
    try:
        # Validate product details
        if not data.get("name") or not data.get("total_stock") or not data.get("unit_price"):
            return jsonify({"error": "Missing product details"}), 400

        # Check if product already exists
        existing_product = Inventory.query.filter_by(item_name=data["name"]).first()
        if existing_product:
            # Auto-restock instead of creating a duplicate
            existing_product.total_stock += data["total_stock"]
        else:
            # Add new product
            product = Inventory(
                item_name=data["name"],
                category=data["category"],
                subcategory=data.get("subcategory"),
                product_code=data.get("product_code"),
                unit_price=data["unit_price"],
                total_stock=data["total_stock"]
            )
            db.session.add(product)

        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return jsonify({"error": "Failed to add product"}), 500

def delete_product_service(product_id):
    try:
        product = Inventory.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting product: {e}")
        return jsonify({"error": "Failed to delete product"}), 500

def update_stock_service(product_id, quantity_sold):
    try:
        product = Inventory.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Update stock and trigger low-stock alerts
        product.total_stock -= quantity_sold
        if product.total_stock <= 5:  # Low stock threshold
            send_low_stock_alert(product.item_name, product.total_stock)

        db.session.commit()
        return jsonify({"message": "Stock updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating stock: {e}")
        return jsonify({"error": "Failed to update stock"}), 500

def send_low_stock_alert(product_name, remaining_stock):
    """
    Send a low-stock alert to the admin.
    """
    msg = f"⚠ Low Stock Alert: {product_name} has only {remaining_stock} items left."
    # Replace with actual email-sending logic
    logging.warning(msg)
