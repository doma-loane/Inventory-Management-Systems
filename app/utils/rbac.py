from flask_login import current_user
from functools import wraps
from flask import jsonify

def role_required(role):
    """
    Middleware to enforce role-based access control.
    :param role: The required role for the route
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return jsonify({"error": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator
