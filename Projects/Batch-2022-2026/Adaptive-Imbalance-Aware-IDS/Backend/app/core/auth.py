"""
JWT authentication and password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import API_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from app.database import get_db
from app.models import UserDB

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, API_SECRET_KEY or "secret", algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, API_SECRET_KEY or "secret", algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None


def get_user_by_username(db: Session, username: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.username == username, UserDB.is_active == 1).first()


def create_user(db: Session, username: str, email: str, password: str, role: str = "analyst") -> UserDB:
    user = UserDB(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
