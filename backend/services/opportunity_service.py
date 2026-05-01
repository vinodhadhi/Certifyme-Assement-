from datetime import date

from extensions import db
from models.opportunity_model import Opportunity
from utils.validators import validate_opportunity_data


class OpportunityService:

    # ------------------------------------------------------------------ #
    # Get all (current admin only)                                         #
    # ------------------------------------------------------------------ #
    @staticmethod
    def get_all(admin_id: int) -> tuple[dict, int]:
        opportunities = (
            Opportunity.query.filter_by(admin_id=admin_id)
            .order_by(Opportunity.created_at.desc())
            .all()
        )
        return {
            "success": True,
            "message": "Opportunities fetched successfully.",
            "data": [o.to_dict() for o in opportunities],
            "total": len(opportunities),
        }, 200

    # ------------------------------------------------------------------ #
    # Get single (with ownership check)                                    #
    # ------------------------------------------------------------------ #
    @staticmethod
    def get_one(opportunity_id: int, admin_id: int) -> tuple[dict, int]:
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"success": False, "message": "Opportunity not found."}, 404
        if opportunity.admin_id != admin_id:
            return {"success": False, "message": "Access denied. This opportunity belongs to another account."}, 403

        return {
            "success": True,
            "message": "Opportunity fetched successfully.",
            "data": opportunity.to_dict(),
        }, 200

    # ------------------------------------------------------------------ #
    # Create                                                               #
    # ------------------------------------------------------------------ #
    @staticmethod
    def create(data: dict, admin_id: int) -> tuple[dict, int]:
        errors = validate_opportunity_data(data)
        if errors:
            return {"success": False, "message": "Validation failed.", "errors": errors}, 400

        max_applicants = data.get("max_applicants")
        if max_applicants is not None and max_applicants != "":
            max_applicants = int(max_applicants)
        else:
            max_applicants = None

        opportunity = Opportunity(
            admin_id=admin_id,
            name=data["name"].strip(),
            duration=data["duration"].strip(),
            start_date=date.fromisoformat(str(data["start_date"])),
            description=data["description"].strip(),
            skills=data["skills"].strip(),
            category=data["category"],
            future_opportunities=bool(data.get("future_opportunities", False)),
            max_applicants=max_applicants,
        )
        db.session.add(opportunity)
        db.session.commit()

        return {
            "success": True,
            "message": "Opportunity created successfully.",
            "data": opportunity.to_dict(),
        }, 201

    # ------------------------------------------------------------------ #
    # Update (with ownership check)                                        #
    # ------------------------------------------------------------------ #
    @staticmethod
    def update(opportunity_id: int, data: dict, admin_id: int) -> tuple[dict, int]:
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"success": False, "message": "Opportunity not found."}, 404
        if opportunity.admin_id != admin_id:
            return {"success": False, "message": "Access denied. You can only edit your own opportunities."}, 403

        errors = validate_opportunity_data(data)
        if errors:
            return {"success": False, "message": "Validation failed.", "errors": errors}, 400

        max_applicants = data.get("max_applicants")
        if max_applicants is not None and max_applicants != "":
            max_applicants = int(max_applicants)
        else:
            max_applicants = None

        opportunity.name = data["name"].strip()
        opportunity.duration = data["duration"].strip()
        opportunity.start_date = date.fromisoformat(str(data["start_date"]))
        opportunity.description = data["description"].strip()
        opportunity.skills = data["skills"].strip()
        opportunity.category = data["category"]
        opportunity.future_opportunities = bool(data.get("future_opportunities", False))
        opportunity.max_applicants = max_applicants

        db.session.commit()

        return {
            "success": True,
            "message": "Opportunity updated successfully.",
            "data": opportunity.to_dict(),
        }, 200

    # ------------------------------------------------------------------ #
    # Delete (with ownership check)                                        #
    # ------------------------------------------------------------------ #
    @staticmethod
    def delete(opportunity_id: int, admin_id: int) -> tuple[dict, int]:
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"success": False, "message": "Opportunity not found."}, 404
        if opportunity.admin_id != admin_id:
            return {"success": False, "message": "Access denied. You can only delete your own opportunities."}, 403

        db.session.delete(opportunity)
        db.session.commit()

        return {
            "success": True,
            "message": "Opportunity deleted successfully.",
        }, 200
