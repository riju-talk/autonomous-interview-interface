"""Simplified authentication helpers for development."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.crud.user import user as crud_user


async def get_current_user_optional(
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user (optional for development)."""
    # For development, create a default user if none exists
    default_email = "dev@example.com"
    user = await crud_user.get_by_email(db, email=default_email)
    
    if not user:
        # Create a default development user
        user_data = {
            "email": default_email,
            "username": "dev_user",
            "full_name": "Development User",
            "is_active": True,
            "is_superuser": True
        }
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user_optional),
) -> User:
    """Get current active user."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user