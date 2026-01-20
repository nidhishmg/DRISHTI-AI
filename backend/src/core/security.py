from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuration (Hardcoded for Demo/Phase 3 speed)
SECRET_KEY = "reality_gap_demo_secret_key_change_in_prod"
REFRESH_SECRET_KEY = "reality_gap_demo_refresh_secret_key_change_in_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Redis for Revocation (Mock/Connect)
import redis.asyncio as redis
try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
except Exception:
    print("Redis not available, falling back to in-memory set for revocation.")
    redis_client = None

# Fallback in-memory revocation (for demo validation if Redis down)
_revoked_tokens = set()

async def is_token_revoked(token: str) -> bool:
    if redis_client:
        try:
            return await redis_client.get(f"revoked:{token}") is not None
        except Exception:
            pass
    return token in _revoked_tokens

async def revoke_token(token: str, expires_in: int):
    if redis_client:
        try:
            await redis_client.setex(f"revoked:{token}", expires_in, "true")
            return
        except Exception:
            pass
    _revoked_tokens.add(token)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class User(BaseModel):
    username: str
    role: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token with role claims."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT and extract user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if await is_token_revoked(token):
             raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    return token_data

def require_role(allowed_roles: List[str]):
    """RBAC dependency."""
    async def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role"
            )
        return user
    return role_checker
