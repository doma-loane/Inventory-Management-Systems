from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    return {"message": "Inventory endpoint is working!"}, 200
