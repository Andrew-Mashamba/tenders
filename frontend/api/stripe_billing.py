"""
Stripe billing: Checkout sessions, Customer Portal, webhooks.
"""
import stripe
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, FRONTEND_URL
from database import get_db, User, Plan
from auth import get_current_user, user_to_dict

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/api/billing", tags=["billing"])


@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    """List all available plans."""
    plans = db.query(Plan).all()
    return {
        "plans": [
            {
                "id": p.id,
                "name": p.name,
                "price_monthly": p.price_monthly,
                "max_institutions": p.max_institutions,
                "max_applications_per_month": p.max_applications_per_month,
                "can_download_documents": p.can_download_documents,
                "can_control_scraper": p.can_control_scraper,
                "has_api_access": p.has_api_access,
                "has_email_alerts": p.has_email_alerts,
            }
            for p in plans
        ]
    }


@router.post("/checkout")
def create_checkout(
    plan_id: str = "pro",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe Checkout session for upgrading."""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(503, "Stripe is not configured")

    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan or not plan.stripe_price_id:
        raise HTTPException(400, f"Plan '{plan_id}' not available for purchase")

    # Create or get Stripe customer
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.name,
            metadata={"user_id": str(user.id)},
        )
        user.stripe_customer_id = customer.id
        db.commit()

    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        mode="subscription",
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        success_url=f"{FRONTEND_URL}/settings?checkout=success",
        cancel_url=f"{FRONTEND_URL}/pricing?checkout=cancelled",
        metadata={"user_id": str(user.id), "plan_id": plan_id},
    )

    return {"checkout_url": session.url}


@router.post("/portal")
def create_portal(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe Customer Portal session for managing billing."""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(503, "Stripe is not configured")

    if not user.stripe_customer_id:
        raise HTTPException(400, "No billing account found. Subscribe to a plan first.")

    session = stripe.billing_portal.Session.create(
        customer=user.stripe_customer_id,
        return_url=f"{FRONTEND_URL}/settings",
    )

    return {"portal_url": session.url}


@router.get("/status")
def billing_status(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current subscription status."""
    plan = db.query(Plan).filter(Plan.id == user.plan).first()
    return {
        "plan": user.plan,
        "plan_name": plan.name if plan else "Free",
        "subscription_status": user.subscription_status,
        "subscription_ends_at": user.subscription_ends_at.isoformat() if user.subscription_ends_at else None,
        "stripe_customer_id": user.stripe_customer_id,
        "has_subscription": user.stripe_subscription_id is not None,
    }


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events. No auth — verified by signature."""
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(503, "Webhook secret not configured")

    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(400, "Invalid webhook signature")

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(data, db)
    elif event_type == "customer.subscription.updated":
        _handle_subscription_updated(data, db)
    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(data, db)
    elif event_type == "invoice.payment_failed":
        _handle_payment_failed(data, db)

    return {"status": "ok"}


# ── Webhook Handlers ────────────────────────────────────────────────────────

def _handle_checkout_completed(session: dict, db: Session):
    user_id = session.get("metadata", {}).get("user_id")
    plan_id = session.get("metadata", {}).get("plan_id")
    subscription_id = session.get("subscription")

    if not user_id:
        return

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return

    user.plan = plan_id or "pro"
    user.stripe_subscription_id = subscription_id
    user.subscription_status = "active"
    user.updated_at = datetime.utcnow()
    db.commit()


def _handle_subscription_updated(subscription: dict, db: Session):
    customer_id = subscription.get("customer")
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    # Map Stripe price to plan
    items = subscription.get("items", {}).get("data", [])
    if items:
        price_id = items[0].get("price", {}).get("id")
        plan = db.query(Plan).filter(Plan.stripe_price_id == price_id).first()
        if plan:
            user.plan = plan.id

    user.subscription_status = subscription.get("status", "active")
    if subscription.get("current_period_end"):
        user.subscription_ends_at = datetime.fromtimestamp(subscription["current_period_end"])
    user.updated_at = datetime.utcnow()
    db.commit()


def _handle_subscription_deleted(subscription: dict, db: Session):
    customer_id = subscription.get("customer")
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    user.plan = "free"
    user.stripe_subscription_id = None
    user.subscription_status = "cancelled"
    user.updated_at = datetime.utcnow()
    db.commit()


def _handle_payment_failed(invoice: dict, db: Session):
    customer_id = invoice.get("customer")
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    user.subscription_status = "past_due"
    user.updated_at = datetime.utcnow()
    db.commit()
