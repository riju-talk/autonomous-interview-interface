from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import re

from app.schemas.base import ORMModeMixin, IDModelMixin, TimestampMixin

class UserRole(str, Enum):
    """User roles in the system."""
    CANDIDATE = "candidate"
    INTERVIEWER = "interviewer"
    ADMIN = "admin"

class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    role: UserRole = Field(default=UserRole.CANDIDATE, description="User role")
    is_active: bool = Field(default=True, description="Whether the user is active")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """Ensure username contains only alphanumeric characters and underscores."""
        if not re.match(r'^\w+$', v):
            raise ValueError('Username must contain only letters, numbers and underscores')
        return v

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    role: Optional[UserRole] = Field(None, description="User role")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="New password")

class UserInDBBase(UserBase, IDModelMixin, TimestampMixin, ORMModeMixin):
    """Base schema for user stored in DB."""
    class Config:
        from_attributes = True

class UserPublic(UserInDBBase):
    """Schema for public user data (returned in API responses)."""
    pass

class UserInDB(UserInDBBase):
    """Schema for user data stored in the database."""
    hashed_password: str = Field(..., description="Hashed password")
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")

class Token(BaseModel):
    """Schema for access token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Time until token expiration in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")

class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: Optional[int] = Field(None, description="Subject (user ID)")
    exp: Optional[int] = Field(None, description="Expiration timestamp")
    iat: Optional[int] = Field(None, description="Issued at timestamp")
    type: Optional[str] = Field(None, description="Token type (access/refresh)")
    
    class Config:
        from_attributes = True

class UserWithToken(UserPublic):
    """Schema for user data with authentication token."""
    token: Token = Field(..., description="Authentication token")

class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr = Field(..., description="User's email address")

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
