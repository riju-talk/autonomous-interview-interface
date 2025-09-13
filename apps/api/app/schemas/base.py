from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, Any
from datetime import datetime
from enum import Enum

# Generic Type Variable
T = TypeVar('T')

class ResponseStatus(str, Enum):
    """Standard response status values."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    BAD_REQUEST = "bad_request"

class BaseResponse(BaseModel, Generic[T]):
    ""
    Base response model for all API responses.
    
    Attributes:
        status: Response status (success/error)
        data: Response data (if any)
        error: Error details (if any)
        meta: Additional metadata
    """
    status: ResponseStatus = Field(..., description="Response status")
    data: Optional[T] = Field(None, description="Response data")
    error: Optional[dict] = Field(None, description="Error details")
    meta: Optional[dict] = Field(None, description="Additional metadata")
    
    @classmethod
    def success(
        cls, 
        data: Optional[T] = None, 
        meta: Optional[dict] = None
    ) -> 'BaseResponse[T]':
        """Create a success response."""
        return cls(status=ResponseStatus.SUCCESS, data=data, meta=meta)
    
    @classmethod
    def error(
        cls, 
        message: str, 
        code: str = "unknown_error",
        status_code: int = 400,
        details: Optional[dict] = None
    ) -> 'BaseResponse[None]':
        """Create an error response."""
        error_data = {
            "message": message,
            "code": code,
            "status_code": status_code
        }
        if details:
            error_data["details"] = details
            
        return cls(
            status=ResponseStatus.ERROR,
            error=error_data
        )

class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""
    page: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate the offset for database queries."""
        return (self.page - 1) * self.page_size

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

class TimestampMixin(BaseModel):
    """Mixin for models with created_at and updated_at timestamps."""
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class IDModelMixin(BaseModel):
    """Mixin for models with an ID field."""
    id: int = Field(..., description="Unique identifier")

class UUIDModelMixin(BaseModel):
    """Mixin for models with a UUID field."""
    uuid: str = Field(..., description="Unique identifier (UUID)")

class ORMModeMixin(BaseModel):
    """Mixin for enabling ORM mode in Pydantic models."""
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

def to_camel_case(string: str) -> str:
    """Convert snake_case to camelCase."""
    words = string.split('_')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
