"""
Environment-based configuration for TENDERS SaaS backend.
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("TENDERS_PROJECT_ROOT", "/var/www/html/tenders"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://tenders:tenders@localhost:5432/tenders")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production-immediately")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Public catalogue access without login (Bearer token; set via env in production)
STATIC_API_TOKEN = os.getenv("TENDERS_STATIC_API_TOKEN", "").strip()

# Frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://tenders.zimasystems.com")
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,https://tenders.zimasystems.com,https://zimasystems.com,https://www.zimasystems.com",
).split(",")

# Rate limiting
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "5/minute")
