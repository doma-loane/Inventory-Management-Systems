from ..models.inventory import Inventory
from ..models.stock_history import StockHistory
from ..extensions import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class InventoryManager:
    """Handles stock management operations."""

    @staticmethod
    def add_stock(product_id, quantity):
        """Increase stock quantity for a given product."""
        product = Inventory.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        if quantity <= 0:
            return {"error": "Quantity must be positive"}, 400

        product.total_stock += quantity
        InventoryManager.log_stock_change(product_id, quantity, "Stock Added")

        db.session.commit()
        return {"message": f"Stock updated: {product.total_stock} units available"}

    @staticmethod
    def reduce_stock(product_id, quantity):
        """Reduce stock quantity for a product while ensuring stock does not go negative."""
        product = Inventory.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        if quantity <= 0:
            return {"error": "Quantity must be positive"}, 400

        if product.total_stock < quantity:
            return {"error": "Insufficient stock"}, 400

        product.total_stock -= quantity
        InventoryManager.log_stock_change(product_id, -quantity, "Stock Removed")

        db.session.commit()
        return {"message": f"Stock updated: {product.total_stock} units remaining"}

    @staticmethod
    def log_stock_change(product_id, quantity, action):
        """Record stock movement for auditing."""
        history_entry = StockHistory(
            product_id=product_id,
            quantity_changed=quantity,
            action=action,
            timestamp=datetime.utcnow()
        )
        db.session.add(history_entry)

    @staticmethod
    def batch_update_stock(updates):
        """
        Perform batch stock updates.
        :param updates: List of dictionaries with product_id and quantity_change
        """
        try:
            for update in updates:
                product = Inventory.query.get(update["product_id"])
                if not product:
                    raise ValueError(f"Product ID {update['product_id']} not found")

                new_stock = product.total_stock + update["quantity_change"]
                if new_stock < 0:
                    raise ValueError(f"Insufficient stock for Product ID {update['product_id']}")

                product.total_stock = new_stock
                InventoryManager.log_stock_change(
                    update["product_id"],
                    update["quantity_change"],
                    "Batch Update"
                )

            db.session.commit()
            return {"message": "Batch stock update successful"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @staticmethod
    def get_stock_levels():
        """Retrieve all stock levels."""
        products = Inventory.query.all()
        return [
            {
                "id": p.id,
                "name": p.item_name,
                "quantity": p.total_stock,
                "last_updated": p.updated_at
            }
            for p in products
        ]
