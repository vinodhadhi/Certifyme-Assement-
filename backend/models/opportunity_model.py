from extensions import db
from datetime import datetime, timezone


class Opportunity(db.Model):
    __tablename__ = "opportunities"

    CATEGORY_CHOICES = [
        "Technology",
        "Business",
        "Design",
        "Marketing",
        "Data Science",
        "Other",
    ]

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(
        db.Integer, db.ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)          # comma-separated
    category = db.Column(db.String(100), nullable=False)
    future_opportunities = db.Column(db.Boolean, default=False, nullable=False)
    max_applicants = db.Column(db.Integer, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "name": self.name,
            "duration": self.duration,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "description": self.description,
            "skills": [s.strip() for s in self.skills.split(",") if s.strip()],
            "category": self.category,
            "future_opportunities": self.future_opportunities,
            "max_applicants": self.max_applicants,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Opportunity {self.name}>"
