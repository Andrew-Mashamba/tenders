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

# Frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8010,https://zima-uat.site:8007").split(",")

# Rate limiting
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "5/minute")
