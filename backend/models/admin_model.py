from extensions import db
from datetime import datetime, timezone


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    opportunities = db.relationship(
        "Opportunity", backref="admin", lazy=True, cascade="all, delete-orphan"
    )
    password_resets = db.relationship(
        "PasswordReset", backref="admin", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Admin {self.email}>"
