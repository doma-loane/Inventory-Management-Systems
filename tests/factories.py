from app.models.inventory import Inventory
from app.extensions import db
from app.models import Product, Sale
from datetime import datetime

def create_inventory_item(
    item_name="Test Product",
    total_stock=100,
    unit_price=10.0,
    image_path=None,
    category="Sample Category",
    subcategory=None,
    product_code="123456789"
):
    item = Inventory(
        item_name=item_name,
        total_stock=total_stock,
        unit_price=unit_price,
        image_path=image_path,
        category=category,
        subcategory=subcategory,
        product_code=product_code
    )
    db.session.add(item)
    db.session.commit()
    return item

def create_test_product(db, name="Test Product", category="General", price=100.0, quantity=10):
    product = Product(
        name=name,
        category=category,
        price=price,
        quantity=quantity
    )
    db.session.add(product)
    db.session.commit()
    return product

def create_test_sale(db, product_id, quantity_sold=2):
    sale = Sale(
        product_id=product_id,
        quantity=quantity_sold,
        timestamp=datetime.utcnow()
    )
    db.session.add(sale)
    db.session.commit()
    return sale
