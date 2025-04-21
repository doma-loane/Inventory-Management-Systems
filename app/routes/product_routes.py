from flask import Blueprint

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/')
def index():
    return "Product Home"
