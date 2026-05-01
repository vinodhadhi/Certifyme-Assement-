import jwt
from datetime import datetime, timezone
from flask import current_app


def generate_token(admin_id: int, remember_me: bool = False) -> str:
    """Generate a signed JWT access token."""
    if remember_me:
        expiry = current_app.config["JWT_REMEMBER_ME_EXPIRES"]
    else:
        expiry = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    payload = {
        "sub": admin_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + expiry,
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    Returns payload dict on success.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    return jwt.decode(
        token,
        current_app.config["JWT_SECRET_KEY"],
        algorithms=["HS256"],
    )
