import os
from typing import AsyncGenerator, TypeVar, Type, Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
    AsyncConnection,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import NullPool
from sqlalchemy import event
from sqlalchemy.engine.interfaces import DBAPIConnection

from app.core.config import settings

def create_db_engine(url: str, **kwargs: Any) -> AsyncEngine:
    """Create and configure the async SQLAlchemy engine.
    
    Args:
        url: Database connection URL
        **kwargs: Additional engine configuration
        
    Returns:
        Configured async SQLAlchemy engine
    """
    engine = create_async_engine(
        url,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        **kwargs,
    )
    
    # Enable WAL mode for SQLite
    if url.startswith('sqlite'):
        @event.listens_for(engine.sync_engine, 'connect')
        def set_sqlite_pragma(dbapi_connection: DBAPIConnection, _: Any) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA journal_mode=WAL')
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()
    
    return engine

# Create engines
engine = create_db_engine(settings.DATABASE_URL)


def create_session_factory(engine: AsyncEngine) -> sessionmaker:
    """Create a session factory for the given engine.
    
    Args:
        engine: SQLAlchemy async engine
        
    Returns:
        Configured session factory
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

# Create session factories
async_session_factory = create_session_factory(engine)


# Test database configuration
test_engine = create_db_engine(
    settings.TEST_DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,  # Use NullPool for tests to ensure clean state
)


# Create test session factory
test_session_factory = create_session_factory(test_engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session.
    
    Yields:
        AsyncSession: An async database session
        
    Example:
        ```python
        async with get_db() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
        ```
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a test database session.
    
    Yields:
        AsyncSession: An async database session for testing
        
    Example:
        ```python
        async with get_test_db() as session:
            # Test database operations
            pass
        ```
    """
    async with test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

# Create base class for models first to avoid circular imports
Base = declarative_base()

# Import models after Base is defined to ensure proper registration
from app.models.user import User  # noqa: E402
from app.models.interview import (  # noqa: E402
    Question,
    InterviewSession,
    InterviewResponse,
)

# Ensure all models are imported for proper table creation
__all__ = [
    'Base',
    'User',
    'Question',
    'InterviewSession',
    'InterviewResponse',
]

async def init_db() -> None:
    """Initialize database tables.
    
    Note:
        In production, use Alembic migrations instead of this function.
        This is only for development and testing purposes.
    """
    is_test = os.getenv("ENV") == "test"
    current_engine = test_engine if is_test else engine
    
    async with current_engine.begin() as conn:
        if is_test:
            # For tests, drop and create all tables
            await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    if not is_test:
        # Apply any pending migrations in development
        try:
            from alembic import command
            from alembic.config import Config
            
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
        except ImportError:
            pass  # Alembic not available, skip migrations
