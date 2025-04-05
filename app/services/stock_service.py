from ..services.inventory_service import update_stock_service
from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def async_update_stock(product_id, quantity_sold):
    """
    Asynchronously update stock for a product.
    """
    update_stock_service(product_id, quantity_sold)
