from ..extensions import db
from datetime import datetime

class Product(db.Model):
    """Product Model: Stores product details and stock levels."""
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Indexed and unique
    barcode = db.Column(db.String(50), unique=True, nullable=True)  # Indexed and unique
    product_code = db.Column(db.String(50), unique=True, nullable=True)  # Indexed and unique
    quantity = db.Column(db.Integer, default=0, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatic timestamp
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Auto-updated timestamp
    deleted = db.Column(db.Boolean, default=False)  # Soft delete flag

    # Relationship
    stock_history = db.relationship("StockHistory", backref="product", lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Product {self.name} (Code: {self.barcode})>"
