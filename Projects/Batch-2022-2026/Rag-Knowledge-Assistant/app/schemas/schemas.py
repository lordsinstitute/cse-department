from typing import Optional, List
from pydantic import BaseModel


# Auth
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


# Products
class ProductCreate(BaseModel):
    product_id: str
    name: str
    description: str = ""


class ProductResponse(BaseModel):
    id: int
    product_id: str
    name: str
    description: str


# Query
class QueryRequest(BaseModel):
    productId: str
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


# User-Product assignment
class UserProductAssign(BaseModel):
    product_ids: List[str]


# Web Scrape
class ScrapeRequest(BaseModel):
    product_id: str
    url: str
    max_pages: int = 10


# Config
class AppConfigUpdate(BaseModel):
    anthropic_api_key: Optional[str] = None
