from ..extensions import db
from datetime import datetime

class Sale(db.Model):
    """Database model for tracking sales transactions."""
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Consistent timestamp

    product = db.relationship("Product", backref=db.backref("sales", lazy=True))

    def __repr__(self):
        return f"<Sale {self.id}>"