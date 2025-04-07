from ..extensions import db
from datetime import datetime

class StockHistory(db.Model):
    """StockHistory Model: Logs stock changes for auditing."""
    __tablename__ = 'stock_history'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id", ondelete="CASCADE"), nullable=False)  # Foreign key constraint
    quantity_changed = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., "Stock Added", "Stock Removed"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Automatic timestamp

    def __repr__(self):
        return f"<StockHistory {self.action} - {self.quantity_changed} units>"
