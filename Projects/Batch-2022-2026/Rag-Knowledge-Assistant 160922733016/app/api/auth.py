from fastapi import APIRouter, Depends, HTTPException
import sqlite3

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user, require_admin
from app.schemas.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, conn: sqlite3.Connection = Depends(get_db)):
    user = conn.execute("SELECT * FROM users WHERE username = ?", (req.username,)).fetchone()
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"],
        "user_id": user["id"],
    })
    return TokenResponse(access_token=token, role=user["role"], username=user["username"])


@router.post("/users", response_model=UserResponse)
def create_user(
    req: UserCreate,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    existing = conn.execute("SELECT id FROM users WHERE username = ?", (req.username,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    cursor = conn.execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
        (req.username, hash_password(req.password), req.role),
    )
    conn.commit()
    return UserResponse(id=cursor.lastrowid, username=req.username, role=req.role)


@router.get("/users")
def list_users(
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    rows = conn.execute("SELECT id, username, role FROM users").fetchall()
    users = []
    for r in rows:
        assigned = conn.execute(
            "SELECT p.name FROM user_products up JOIN products p ON up.product_id = p.product_id WHERE up.user_id = ?",
            (r["id"],)
        ).fetchall()
        product_names = [a["name"] for a in assigned]
        users.append({
            "id": r["id"],
            "username": r["username"],
            "role": r["role"],
            "assigned_products": product_names,
        })
    return users


@router.post("/users/{user_id}/products")
def assign_products_to_user(
    user_id: int,
    product_ids: list[str],
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    conn.execute("DELETE FROM user_products WHERE user_id = ?", (user_id,))
    for pid in product_ids:
        conn.execute("INSERT INTO user_products (user_id, product_id) VALUES (?, ?)", (user_id, pid))
    conn.commit()
    return {"message": f"Assigned {len(product_ids)} products to user {user_id}"}


@router.get("/users/{user_id}/products")
def get_user_products(
    user_id: int,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    rows = conn.execute("SELECT product_id FROM user_products WHERE user_id = ?", (user_id,)).fetchall()
    return [r["product_id"] for r in rows]


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
