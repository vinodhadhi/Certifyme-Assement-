from functools import wraps
from flask import request, g
import jwt as pyjwt

from utils.jwt_handler import decode_token
from utils.helpers import error_response
from models.admin_model import Admin


def require_auth(f):
    """
    JWT authentication decorator.
    Sets g.current_admin_id and g.current_admin on the Flask request context.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header:
            return error_response("Authorization header missing.", 401)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error_response(
                "Invalid Authorization format. Expected: Bearer <token>", 401
            )

        token = parts[1]

        try:
            payload = decode_token(token)
        except pyjwt.ExpiredSignatureError:
            return error_response("Token has expired. Please log in again.", 401)
        except pyjwt.InvalidTokenError:
            return error_response("Invalid token. Please log in again.", 401)

        admin_id = payload.get("sub")
        if not admin_id:
            return error_response("Invalid token payload.", 401)

        admin = Admin.query.get(admin_id)
        if not admin:
            return error_response("Admin account not found.", 401)

        g.current_admin_id = admin_id
        g.current_admin = admin

        return f(*args, **kwargs)

    return decorated
