from flask import Blueprint, request, g, jsonify
from middleware.auth_middleware import require_auth
from services.opportunity_service import OpportunityService

opportunity_bp = Blueprint("opportunities", __name__)


@opportunity_bp.route("", methods=["GET"])
@require_auth
def get_all():
    """
    US-2.1 — View All Opportunities (current admin only)
    GET /api/opportunities
    """
    result, status = OpportunityService.get_all(g.current_admin_id)
    return jsonify(result), status


@opportunity_bp.route("/<int:opportunity_id>", methods=["GET"])
@require_auth
def get_one(opportunity_id):
    """
    US-2.4 — View Opportunity Details
    GET /api/opportunities/<id>
    """
    result, status = OpportunityService.get_one(opportunity_id, g.current_admin_id)
    return jsonify(result), status


@opportunity_bp.route("", methods=["POST"])
@require_auth
def create():
    """
    US-2.2 — Add a New Opportunity
    POST /api/opportunities
    Body: { name, duration, start_date, description, skills, category,
            future_opportunities, max_applicants? }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    result, status = OpportunityService.create(data, g.current_admin_id)
    return jsonify(result), status


@opportunity_bp.route("/<int:opportunity_id>", methods=["PUT"])
@require_auth
def update(opportunity_id):
    """
    US-2.5 — Edit an Opportunity
    PUT /api/opportunities/<id>
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    result, status = OpportunityService.update(opportunity_id, data, g.current_admin_id)
    return jsonify(result), status


@opportunity_bp.route("/<int:opportunity_id>", methods=["DELETE"])
@require_auth
def delete(opportunity_id):
    """
    US-2.6 — Delete an Opportunity
    DELETE /api/opportunities/<id>
    """
    result, status = OpportunityService.delete(opportunity_id, g.current_admin_id)
    return jsonify(result), status
