from flask import Blueprint, request, jsonify

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('username') == 'admin' and data.get('password') == 'adminpass':
        return jsonify({"message": "Welcome to the Dashboard!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
