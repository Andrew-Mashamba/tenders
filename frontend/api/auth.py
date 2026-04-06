"""
Authentication: JWT tokens, password hashing, FastAPI dependencies.
"""
import hashlib
import json
import secrets
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from database import get_db, User, RefreshToken, Plan

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Password Utilities ──────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def hash_token(token: str) -> str:
    """Fast SHA-256 hash for refresh tokens (not passwords)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_token(token: str, token_hash: str) -> bool:
    return hashlib.sha256(token.encode("utf-8")).hexdigest() == token_hash


# ── JWT Utilities ───────────────────────────────────────────────────────────

def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "email": email, "exp": expire, "type": "access"},
        JWT_SECRET, algorithm=JWT_ALGORITHM
    )


def create_refresh_token_value() -> str:
    return secrets.token_urlsafe(64)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError("Not an access token")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── FastAPI Dependencies ────────────────────────────────────────────────────

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Returns user if authenticated, None otherwise. For endpoints that work with or without auth."""
    if token is None:
        return None
    try:
        payload = decode_access_token(token)
        return db.query(User).filter(User.id == int(payload["sub"])).first()
    except HTTPException:
        return None


# ── Request/Response Schemas ────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    company: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    company_profile: Optional[dict] = None


# ── Helper ──────────────────────────────────────────────────────────────────

def user_to_dict(user: User, db: Session) -> dict:
    plan = db.query(Plan).filter(Plan.id == user.plan).first()
    followed_count = len(user.institutions)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "company": user.company,
        "company_profile": json.loads(user.company_profile) if user.company_profile else None,
        "plan": user.plan,
        "plan_name": plan.name if plan else "Free",
        "subscription_status": user.subscription_status,
        "subscription_ends_at": user.subscription_ends_at.isoformat() if user.subscription_ends_at else None,
        "applications_this_month": user.applications_this_month,
        "followed_institutions": followed_count,
        "max_institutions": plan.max_institutions if plan else 10,
        "max_applications_per_month": plan.max_applications_per_month if plan else 5,
        "can_download_documents": plan.can_download_documents if plan else False,
        "can_control_scraper": plan.can_control_scraper if plan else False,
        "is_admin": user.is_admin,
        "email_verified": user.email_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def _issue_tokens(user: User, db: Session) -> TokenResponse:
    access = create_access_token(user.id, user.email)
    refresh_value = create_refresh_token_value()

    # Store refresh token hash
    rt = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_value),
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(rt)
    db.commit()

    return TokenResponse(
        access_token=access,
        refresh_token=refresh_value,
        user=user_to_dict(user, db),
    )


# ── Auth Endpoints ──────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if len(req.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    existing = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if existing:
        raise HTTPException(409, "Email already registered")

    user = User(
        email=req.email.lower().strip(),
        password_hash=hash_password(req.password),
        name=req.name,
        company=req.company,
        plan="free",
        applications_reset_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return _issue_tokens(user, db)


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    return _issue_tokens(user, db)


@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    # Find a valid refresh token
    tokens = db.query(RefreshToken).filter(
        RefreshToken.expires_at > datetime.utcnow()
    ).all()

    lookup_hash = hash_token(req.refresh_token)
    matched_token = None
    for rt in tokens:
        if rt.token_hash == lookup_hash:
            matched_token = rt
            break

    if not matched_token:
        raise HTTPException(401, "Invalid or expired refresh token")

    user = db.query(User).filter(User.id == matched_token.user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    # Rotate: delete old token, issue new pair
    db.delete(matched_token)
    db.commit()

    return _issue_tokens(user, db)


@router.post("/logout")
def logout(
    req: RefreshRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Invalidate the refresh token
    lookup_hash = hash_token(req.refresh_token)
    rt = db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.token_hash == lookup_hash,
    ).first()
    if rt:
        db.delete(rt)
        db.commit()
    return {"status": "ok"}


@router.get("/me")
def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_to_dict(user, db)


@router.put("/me")
def update_me(
    req: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if req.name is not None:
        user.name = req.name
    if req.company is not None:
        user.company = req.company
    if req.company_profile is not None:
        user.company_profile = json.dumps(req.company_profile)
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user_to_dict(user, db)
