import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from jose import JWTError, jwt as jose_jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.token import TokenData
from app.schemas.user import UserCreate, UserInDB, UserUpdate

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a password hash."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jose_jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jose_jwt.encode(
            to_encode, settings.JWT_REFRESH_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, secret: str) -> Dict[str, Any]:
        """Verify a JWT token."""
        try:
            payload = jose_jwt.decode(
                token, secret, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """Get the current authenticated user from the JWT token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = AuthService.verify_token(token, settings.JWT_SECRET)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
            
        # Get user from database
        user = await User.get_by_username(db, username=token_data.username)
        if user is None:
            raise credentials_exception
            
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        
        return user

    @staticmethod
    async def get_current_active_user(
        current_user: User = Depends(get_current_user),
    ) -> User:
        """Get the current active user."""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    @staticmethod
    async def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
    ) -> User:
        """Get the current active superuser."""
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=400, detail="The user doesn't have enough privileges"
            )
        return current_user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = await User.get_by_username(db, username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user."""
        hashed_password = AuthService.get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_active=True,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(
        db: AsyncSession, db_user: User, user_in: UserUpdate
    ) -> User:
        """Update a user."""
        update_data = user_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = AuthService.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user

# Create a global instance of the auth service
auth_service = AuthService()
