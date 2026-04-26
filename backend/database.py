"""
SQLAlchemy models and database setup for TENDERS SaaS.
"""
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean,
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


# ── Models ──────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    company = Column(String)
    company_profile = Column(Text)  # JSON: rich company info for AI-generated applications
    plan = Column(String, default="free")
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    subscription_status = Column(String, default="active")
    subscription_ends_at = Column(DateTime)
    applications_this_month = Column(Integer, default=0)
    applications_reset_at = Column(DateTime)
    is_admin = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    email_verify_token = Column(String)
    password_reset_token = Column(String)
    password_reset_expires = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    institutions = relationship("UserInstitution", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("UserApplication", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class UserInstitution(Base):
    __tablename__ = "user_institutions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    institution_slug = Column(String, nullable=False, primary_key=True)
    followed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="institutions")


class UserApplication(Base):
    __tablename__ = "user_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tender_id = Column(String, nullable=False)
    institution_slug = Column(String, nullable=False)
    status = Column(String, default="interested")
    notes = Column(Text)
    pdf_path = Column(String)
    submitted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "tender_id"),)

    user = relationship("User", back_populates="applications")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price_monthly = Column(Integer, nullable=False)
    stripe_price_id = Column(String)
    max_institutions = Column(Integer, nullable=False)
    max_applications_per_month = Column(Integer, nullable=False)
    can_download_documents = Column(Boolean, default=False)
    can_control_scraper = Column(Boolean, default=False)
    has_api_access = Column(Boolean, default=False)
    has_email_alerts = Column(Boolean, default=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")


# ── Database Lifecycle ──────────────────────────────────────────────────────

def create_tables():
    """Create all tables and seed default plans."""
    Base.metadata.create_all(bind=engine)
    seed_plans()


def seed_plans():
    """Insert default plans if they don't exist."""
    db = SessionLocal()
    try:
        if db.query(Plan).count() == 0:
            plans = [
                Plan(
                    id="free", name="Free", price_monthly=0,
                    max_institutions=10, max_applications_per_month=5,
                    can_download_documents=False, can_control_scraper=False,
                    has_api_access=False, has_email_alerts=False,
                ),
                Plan(
                    id="pro", name="Pro", price_monthly=2900,
                    max_institutions=100, max_applications_per_month=999999,
                    can_download_documents=True, can_control_scraper=False,
                    has_api_access=False, has_email_alerts=True,
                ),
                Plan(
                    id="enterprise", name="Enterprise", price_monthly=9900,
                    max_institutions=999999, max_applications_per_month=999999,
                    can_download_documents=True, can_control_scraper=True,
                    has_api_access=True, has_email_alerts=True,
                ),
            ]
            db.add_all(plans)
            db.commit()
    finally:
        db.close()


def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
