from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import User, UserLogin, TokenData
from .database import get_session
import os

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key - should be set in environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7change_this_to_a_secure_random_key")  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    try:
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
        return pwd_context.verify(truncated_password, hashed_password)
    except Exception as e:
        # If bcrypt verification fails, it might be a different hash format
        # In that case, we could try alternative methods if needed
        import hashlib
        # Try SHA256 comparison as a fallback
        if hashed_password == hashlib.sha256(plain_password.encode('utf-8')).hexdigest():
            return True
        return False

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    try:
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = password[:72] if len(password) > 72 else password
        return pwd_context.hash(truncated_password)
    except:
        # If bcrypt fails, use SHA256 as fallback
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """Get the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user (can be extended for active/inactive checks)."""
    return current_user