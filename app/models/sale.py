from ..extensions import db
from datetime import datetime, timezone

class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), index=True, unique=True)  # Indexed field for faster lookups
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))