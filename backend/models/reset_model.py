from extensions import db
from datetime import datetime, timezone


class PasswordReset(db.Model):
    __tablename__ = "password_resets"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(
        db.Integer, db.ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at.replace(tzinfo=timezone.utc)

    def __repr__(self):
        return f"<PasswordReset admin_id={self.admin_id}>"
