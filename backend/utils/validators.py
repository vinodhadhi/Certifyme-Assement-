import re
from datetime import date
from models.opportunity_model import Opportunity


EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> str | None:
    """Returns error string or None."""
    if not email or not email.strip():
        return "Email is required."
    if not EMAIL_REGEX.match(email.strip()):
        return "Invalid email format."
    return None


def validate_password(password: str) -> str | None:
    if not password:
        return "Password is required."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


def validate_signup_data(data: dict) -> dict:
    """Returns dict of field -> error message. Empty dict means valid."""
    errors = {}

    email_err = validate_email(data.get("email", ""))
    if email_err:
        errors["email"] = email_err

    password = data.get("password", "")
    pw_err = validate_password(password)
    if pw_err:
        errors["password"] = pw_err

    confirm = data.get("confirm_password", "")
    if not confirm:
        errors["confirm_password"] = "Please confirm your password."
    elif password and password != confirm:
        errors["confirm_password"] = "Passwords do not match."

    full_name = data.get("full_name", "").strip()
    if not full_name:
        errors["full_name"] = "Full name is required."
    elif len(full_name) < 2:
        errors["full_name"] = "Full name must be at least 2 characters."

    return errors


def validate_opportunity_data(data: dict) -> dict:
    """Returns dict of field -> error message."""
    errors = {}

    if not data.get("name", "").strip():
        errors["name"] = "Opportunity name is required."

    if not data.get("duration", "").strip():
        errors["duration"] = "Duration is required."

    start_date_str = data.get("start_date", "")
    if not start_date_str:
        errors["start_date"] = "Start date is required."
    else:
        try:
            date.fromisoformat(str(start_date_str))
        except ValueError:
            errors["start_date"] = "Start date must be a valid date (YYYY-MM-DD)."

    if not data.get("description", "").strip():
        errors["description"] = "Description is required."

    if not data.get("skills", "").strip():
        errors["skills"] = "At least one skill is required."

    category = data.get("category", "")
    if not category:
        errors["category"] = "Category is required."
    elif category not in Opportunity.CATEGORY_CHOICES:
        errors["category"] = (
            f"Invalid category. Must be one of: {', '.join(Opportunity.CATEGORY_CHOICES)}"
        )

    max_applicants = data.get("max_applicants")
    if max_applicants is not None and max_applicants != "":
        try:
            val = int(max_applicants)
            if val < 1:
                errors["max_applicants"] = "Max applicants must be a positive integer."
        except (ValueError, TypeError):
            errors["max_applicants"] = "Max applicants must be a valid number."

    return errors
