from ..extensions import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Indexed field
    total_stock = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    subcategory = db.Column(db.String(100), nullable=True)
    product_code = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return f"<Inventory {self.item_name} - {self.product_code}>"