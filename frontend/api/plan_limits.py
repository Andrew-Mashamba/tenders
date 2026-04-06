"""
Plan-based feature gating and limit checking.
"""
from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, User, Plan, UserInstitution, UserApplication
from auth import get_current_user


def _get_plan(user: User, db: Session) -> Plan:
    plan = db.query(Plan).filter(Plan.id == user.plan).first()
    if not plan:
        plan = db.query(Plan).filter(Plan.id == "free").first()
    return plan


def _reset_monthly_counter_if_needed(user: User, db: Session):
    """Reset the monthly application counter if a new month has started."""
    now = datetime.utcnow()
    if user.applications_reset_at is None or user.applications_reset_at.month != now.month:
        user.applications_this_month = 0
        user.applications_reset_at = now
        db.commit()


def check_institution_limit(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dependency: raises 403 if user has reached institution follow limit."""
    plan = _get_plan(user, db)
    count = db.query(UserInstitution).filter(UserInstitution.user_id == user.id).count()
    if count >= plan.max_institutions:
        raise HTTPException(
            403,
            {
                "error": "institution_limit",
                "message": f"Your {plan.name} plan allows following {plan.max_institutions} institutions. Upgrade to follow more.",
                "current": count,
                "limit": plan.max_institutions,
                "plan": user.plan,
            }
        )
    return user


def check_application_limit(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dependency: raises 403 if user has reached monthly application limit."""
    plan = _get_plan(user, db)
    _reset_monthly_counter_if_needed(user, db)
    if user.applications_this_month >= plan.max_applications_per_month:
        raise HTTPException(
            403,
            {
                "error": "application_limit",
                "message": f"Your {plan.name} plan allows {plan.max_applications_per_month} applications per month. Upgrade for more.",
                "current": user.applications_this_month,
                "limit": plan.max_applications_per_month,
                "plan": user.plan,
            }
        )
    return user


def check_download_access(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dependency: raises 403 if user's plan doesn't allow document downloads."""
    plan = _get_plan(user, db)
    if not plan.can_download_documents:
        raise HTTPException(
            403,
            {
                "error": "feature_locked",
                "message": "Document downloads require a Pro or Enterprise plan.",
                "feature": "download_documents",
                "plan": user.plan,
            }
        )
    return user


def check_scraper_access(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dependency: raises 403 if user's plan doesn't allow scraper control."""
    plan = _get_plan(user, db)
    if not plan.can_control_scraper:
        raise HTTPException(
            403,
            {
                "error": "feature_locked",
                "message": "Scraper control requires an Enterprise plan.",
                "feature": "scraper_control",
                "plan": user.plan,
            }
        )
    return user


def get_user_plan_info(user: User, db: Session) -> dict:
    """Get plan details and current usage for a user."""
    plan = _get_plan(user, db)
    _reset_monthly_counter_if_needed(user, db)
    followed = db.query(UserInstitution).filter(UserInstitution.user_id == user.id).count()
    return {
        "plan_id": plan.id,
        "plan_name": plan.name,
        "price_monthly": plan.price_monthly,
        "institutions_used": followed,
        "institutions_limit": plan.max_institutions,
        "applications_used": user.applications_this_month,
        "applications_limit": plan.max_applications_per_month,
        "can_download_documents": plan.can_download_documents,
        "can_control_scraper": plan.can_control_scraper,
        "has_api_access": plan.has_api_access,
        "has_email_alerts": plan.has_email_alerts,
    }
