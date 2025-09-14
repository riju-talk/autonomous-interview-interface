"""CRUD operations for User model."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User, dict, dict]):
    """CRUD operations for User."""
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_github_id(self, db: AsyncSession, *, github_id: int) -> Optional[User]:
        """Get user by GitHub ID."""
        result = await db.execute(select(User).filter(User.github_id == github_id))
        return result.scalar_one_or_none()


# Create instance
user = CRUDUser(User)