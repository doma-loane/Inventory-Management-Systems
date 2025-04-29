from datetime import datetime
from ..extensions import db

class StockHistory(db.Model):
    __tablename__ = 'stock_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete='CASCADE'), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(200))
    
    product = db.relationship('Inventory', back_populates='stock_history')
