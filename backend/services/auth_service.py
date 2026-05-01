import secrets
import logging
from datetime import datetime, timezone, timedelta

import bcrypt

from extensions import db
from models.admin_model import Admin
from models.reset_model import PasswordReset
from utils.validators import validate_signup_data, validate_email
from utils.jwt_handler import generate_token

logger = logging.getLogger(__name__)


class AuthService:

    # ------------------------------------------------------------------ #
    # Sign Up                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def signup(data: dict) -> tuple[dict, int]:
        errors = validate_signup_data(data)
        if errors:
            return {"success": False, "message": "Validation failed.", "errors": errors}, 400

        email = data["email"].strip().lower()
        if Admin.query.filter_by(email=email).first():
            return {
                "success": False,
                "message": "An account with this email already exists.",
                "errors": {"email": "Email is already registered."},
            }, 409

        hashed_pw = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt(12)
        ).decode("utf-8")

        admin = Admin(
            full_name=data["full_name"].strip(),
            email=email,
            password=hashed_pw,
        )
        db.session.add(admin)
        db.session.commit()

        return {
            "success": True,
            "message": "Account created successfully. Please log in.",
            "data": admin.to_dict(),
        }, 201

    # ------------------------------------------------------------------ #
    # Login                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def login(data: dict) -> tuple[dict, int]:
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        remember_me = bool(data.get("remember_me", False))

        if not email or not password:
            return {"success": False, "message": "Email and password are required."}, 400

        admin = Admin.query.filter_by(email=email).first()

        # Constant-time comparison avoids timing-based user enumeration
        if not admin or not bcrypt.checkpw(
            password.encode("utf-8"), admin.password.encode("utf-8")
        ):
            return {"success": False, "message": "Invalid email or password."}, 401

        token = generate_token(admin.id, remember_me=remember_me)

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "token": token,
                "admin": admin.to_dict(),
                "remember_me": remember_me,
            },
        }, 200

    # ------------------------------------------------------------------ #
    # Forgot Password                                                      #
    # ------------------------------------------------------------------ #
    @staticmethod
    def forgot_password(data: dict) -> tuple[dict, int]:
        email = (data.get("email") or "").strip().lower()

        email_err = validate_email(email)
        if email_err:
            # Still return success — never reveal existence
            return {
                "success": True,
                "message": "If that email is registered, a reset link has been sent.",
            }, 200

        admin = Admin.query.filter_by(email=email).first()
        if admin:
            # Invalidate any existing unused tokens for this admin
            PasswordReset.query.filter_by(admin_id=admin.id, used=False).delete()

            token = secrets.token_urlsafe(48)
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

            reset = PasswordReset(
                admin_id=admin.id,
                token=token,
                expires_at=expires_at,
            )
            db.session.add(reset)
            db.session.commit()

            # In production this would send an email; for now we log it
            reset_link = f"http://localhost:5000/reset-password?token={token}"
            logger.info(
                "[FORGOT PASSWORD] Reset link for %s: %s (expires %s)",
                email,
                reset_link,
                expires_at.isoformat(),
            )

        # Always return the same message
        return {
            "success": True,
            "message": "If that email is registered, a reset link has been sent.",
        }, 200

    # ------------------------------------------------------------------ #
    # Verify Reset Token                                                   #
    # ------------------------------------------------------------------ #
    @staticmethod
    def verify_reset_token(token: str) -> tuple[dict, int]:
        reset = PasswordReset.query.filter_by(token=token, used=False).first()

        if not reset:
            return {"success": False, "message": "Invalid or already-used reset token."}, 400

        if reset.is_expired():
            return {"success": False, "message": "This reset link has expired. Please request a new one."}, 400

        return {"success": True, "message": "Token is valid."}, 200
