"""
Authentication: login, register, JWT dependency.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import JWT_EXPIRE_MINUTES, REQUIRE_AUTH
from app.core.auth import (
    create_access_token,
    create_user,
    decode_token,
    get_user_by_username,
    verify_password,
)
from app.database import get_db
from app.models import Token, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Return user id if valid token; else None. Use when auth is optional."""
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload or "sub" not in payload:
        return None
    user = get_user_by_username(db, payload["sub"])
    return user


def get_current_user_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Require valid JWT; return user or 401."""
    if not REQUIRE_AUTH:
        return None
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Login with username/password; returns JWT."""
    user = get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=JWT_EXPIRE_MINUTES),
    )
    return Token(
        access_token=token,
        token_type="bearer",
        expires_in=JWT_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (analyst)."""
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(
        db, user_in.username, user_in.email, user_in.password, user_in.role
    )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=bool(user.is_active),
        created_at=user.created_at,
    )
