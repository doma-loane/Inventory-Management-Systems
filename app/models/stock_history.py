from ..extensions import db
from datetime import datetime

class StockHistory(db.Model):
    """Database model for tracking stock changes."""
    __tablename__ = 'stock_history'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity_changed = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., "Stock Added", "Stock Removed"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Inventory", backref=db.backref("stock_history", lazy=True))

    def __repr__(self):
        return f"<StockHistory Product ID: {self.product_id}, Action: {self.action}>"
