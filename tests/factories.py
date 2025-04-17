from app.models.inventory import Inventory
from app.extensions import db

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
