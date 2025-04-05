import logging
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from ..models import Sale, Inventory
from ..extensions import db  # Fix circular import by importing db from extensions
from ..utils.rbac import role_required

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales', methods=['GET', 'POST'])
@login_required
@role_required("sales")  # Only users with the "sales" role can process sales
def sales_page():
    try:
        if request.method == 'POST':
            data = request.form
            product_code = data.get("product_code")
            quantity = int(data.get("quantity"))
            payment_method = data.get("payment_method")

            product = Inventory.query.filter_by(product_code=product_code).first()
            if not product or product.total_stock < quantity:
                return jsonify({"error": "Insufficient stock or product not found"}), 400

            product.total_stock -= quantity
            sale = Sale(product_id=product.id, quantity=quantity, payment_method=payment_method)
            db.session.add(sale)
            db.session.commit()
            return jsonify({"message": "Sale processed successfully"}), 200

        return render_template("sales.html")
    except Exception as e:
        logging.error(f"Error processing sale: {e}")
        return jsonify({"error": "Failed to process sale"}), 500