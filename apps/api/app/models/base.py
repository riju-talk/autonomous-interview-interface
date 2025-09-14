from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

@as_declarative()
class Base:
    """Base class for all database models."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically.
        
        Converts CamelCase class name to snake_case table name.
        
        Returns:
            str: The table name in snake_case
        """
        return ''.join(['_' + i.lower() if i.isupper() else i for i in cls.__name__]).lstrip('_')

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            c.name: getattr(self, c.name) 
            for c in self.__table__.columns
        }
        
    def update(self, **kwargs) -> None:
        """Update model attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
