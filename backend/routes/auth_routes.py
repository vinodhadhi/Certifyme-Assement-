from flask import Blueprint, request
from services.auth_service import AuthService
from flask import jsonify

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    US-1.1 — Admin Sign Up
    POST /api/auth/signup
    Body: { full_name, email, password, confirm_password }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    result, status = AuthService.signup(data)
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    US-1.2 — Admin Login
    POST /api/auth/login
    Body: { email, password, remember_me }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    result, status = AuthService.login(data)
    return jsonify(result), status


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """
    US-1.3 — Forgot Password
    POST /api/auth/forgot-password
    Body: { email }
    Always returns success to protect user privacy.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    result, status = AuthService.forgot_password(data)
    return jsonify(result), status


@auth_bp.route("/verify-reset-token", methods=["GET"])
def verify_reset_token():
    """
    GET /api/auth/verify-reset-token?token=<token>
    Returns whether the token is valid/not expired.
    """
    token = request.args.get("token", "").strip()
    if not token:
        return jsonify({"success": False, "message": "Token is required."}), 400

    result, status = AuthService.verify_reset_token(token)
    return jsonify(result), status
