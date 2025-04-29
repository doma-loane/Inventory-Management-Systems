from ..extensions import db
from datetime import datetime, timezone

class Sale(db.Model):
    """Database model for tracking sales transactions."""
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    product = db.relationship('Inventory', back_populates='sales')

    def __repr__(self):
        return f"<Sale {self.id}>"