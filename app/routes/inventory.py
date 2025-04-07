import logging
import uuid
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
from ..models.inventory import Inventory
from ..models.sale import Sale
from ..models.stock_history import StockHistory
from ..extensions import db
from ..utils.rbac import role_required
from ..extensions import cache

inventory_bp = Blueprint('inventory', __name__)

# Utility function for stock change logging
def log_stock_change(product_id, quantity, action):
    """Log stock changes for auditing purposes."""
    stock_entry = StockHistory(product_id=product_id, quantity_changed=quantity, action=action)
    db.session.add(stock_entry)
    db.session.commit()

@inventory_bp.route("/", methods=["GET"])
def home():
    """Render homepage."""
    return render_template("index.html")

@inventory_bp.route("/products", methods=["GET"])
@jwt_required()
@role_required("admin")
@cache.cached(timeout=300)  # Cache the response for 5 minutes
def get_products():
    """Retrieve all products with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        products = Inventory.query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            "products": [
                {
                    "id": p.id,
                    "name": p.item_name,
                    "category": p.category,
                    "subcategory": p.subcategory,
                    "barcode": p.image_path,
                    "product_code": p.product_code,
                    "quantity": p.total_stock,
                    "price": p.unit_price,
                } for p in products.items
            ],
            "total_pages": products.pages,
            "current_page": products.page
        }), 200
    except Exception as e:
        logging.error(f"Error fetching inventory: {e}")
        return jsonify({"error": "Failed to fetch inventory"}), 500

@inventory_bp.route("/products/add", methods=["POST"])
@jwt_required()
@role_required("admin")
def add_product():
    """Add a new product while ensuring barcode and product_code uniqueness."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "category", "price"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # Check if product already exists
        existing_product = Inventory.query.filter(
            (Inventory.image_path == data.get("barcode")) |
            (Inventory.product_code == data.get("product_code"))
        ).first()
        if existing_product:
            return jsonify({"error": "Product already exists! Consider restocking."}), 409

        # Assign a unique product code if none is provided
        product_code = data.get("product_code") or str(uuid.uuid4())[:8]

        # Create new product
        new_product = Inventory(
            item_name=data["name"],
            category=data["category"],
            subcategory=data.get("subcategory"),
            image_path=data.get("barcode"),
            product_code=product_code,
            total_stock=data.get("stock_quantity", 0),
            unit_price=data["price"]
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully!", "product_code": product_code}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error, possibly duplicate entry"}), 400
    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@inventory_bp.route("/products/delete/<int:product_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")  # Only admins can delete products
def delete_product(product_id):
    """Soft delete a product by ID."""
    try:
        product = Inventory.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        product.is_deleted = True  # Mark the product as deleted
        db.session.commit()
        return jsonify({"message": "Product deleted (soft delete applied)"}), 200
    except Exception as e:
        logging.error(f"Error deleting product: {e}")
        return jsonify({"error": "Failed to delete product"}), 500

@inventory_bp.route("/products/update_stock/<int:product_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")  # Only admins can update stock
def update_stock(product_id):
    """Update the stock quantity of a product."""
    try:
        data = request.get_json()
        product = Inventory.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        if "quantity" not in data:
            return jsonify({"error": "Quantity is required"}), 400

        # Prevent negative stock
        if product.total_stock + data["quantity"] < 0:
            return jsonify({"error": "Stock level cannot be negative"}), 400

        product.total_stock += data["quantity"]
        db.session.commit()

        # Log stock update
        log_stock_change(product.id, data["quantity"], "Stock Update")

        return jsonify({"message": "Stock updated successfully", "new_quantity": product.total_stock}), 200
    except Exception as e:
        logging.error(f"Error updating stock: {e}")
        return jsonify({"error": "Failed to update stock"}), 500

@inventory_bp.route("/sales", methods=["POST"])
@jwt_required()
@role_required("admin")  # Only admins can record sales
def record_sale():
    """Record a sale transaction."""
    try:
        data = request.get_json()
        if not data or "product_id" not in data or "quantity_sold" not in data:
            raise BadRequest("Missing required fields")

        product = Inventory.query.get(data["product_id"])
        if not product:
            return jsonify({"error": "Product not found"}), 404

        if product.total_stock < data["quantity_sold"]:
            return jsonify({"error": "Not enough stock available"}), 400

        product.total_stock -= data["quantity_sold"]
        sale = Sale(
            product_id=product.id,
            quantity=data["quantity_sold"],
            total_price=product.unit_price * data["quantity_sold"]
        )

        db.session.add(sale)
        db.session.commit()

        # Log stock reduction
        log_stock_change(product.id, -data["quantity_sold"], "Sale")

        return jsonify({"message": "Sale recorded successfully", "sale_id": sale.id}), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error recording sale: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@inventory_bp.route("/search_product", methods=["GET"])
@jwt_required()
@role_required("admin")  # Only admins can search products
def search_product():
    """Search for a product by barcode, product code, or name."""
    try:
        query = request.args.get("query", "").strip()

        if not query:
            return jsonify({"error": "Search query is required"}), 400

        # Search for the product using indexed fields
        product = Inventory.query.filter(
            (Inventory.image_path == query) | 
            (Inventory.product_code == query) | 
            (Inventory.item_name.ilike(f"%{query}%"))
        ).first()

        if not product or product.is_deleted:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "id": product.id,
            "name": product.item_name,
            "barcode": product.image_path,
            "product_code": product.product_code,
            "category": product.category,
            "subcategory": product.subcategory,
            "stock_quantity": product.total_stock,
            "price": product.unit_price
        }), 200
    except Exception as e:
        logging.error(f"Error searching for product: {e}")
        return jsonify({"error": "Failed to search for product"}), 500

@inventory_bp.route("/product_search", methods=["GET"])
@jwt_required()
@role_required("admin")  # Only admins can access the product search page
def product_search():
    """Render the product search page."""
    return render_template("product_search.html")

@inventory_bp.route("/update_stock", methods=["GET"])
@jwt_required()
@role_required("admin")  # Only admins can access the stock update page
def update_stock_page():
    """Render the stock update page."""
    return render_template("update_stock.html")