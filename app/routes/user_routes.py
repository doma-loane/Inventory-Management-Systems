from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    return {"message": "User endpoint is working!"}, 200
