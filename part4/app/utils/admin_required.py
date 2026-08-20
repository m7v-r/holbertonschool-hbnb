from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()

            if not claims.get("is_admin", False):
                return {"error": "Admin privileges required"}, 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
