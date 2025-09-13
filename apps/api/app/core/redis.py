from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from functools import wraps
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

import aioredis
from pydantic import BaseModel

from app.core.config import settings

# Type variables
T = TypeVar('T')
P = TypeVar('P', str, int, float, bool, Dict[str, Any], List[Any])

# Custom types
RedisValue = Union[str, bytes, int, float, bool, Dict[str, Any], List[Any], BaseModel]
RedisEncodable = Union[str, bytes, int, float, bool, Dict[str, Any], List[Any]]

logger = logging.getLogger(__name__)

class RedisClient:
    """A Redis client wrapper with connection pooling and utility methods.
    
    This class implements the singleton pattern to ensure only one Redis connection
    pool is used throughout the application.
    """
    _instance: Optional['RedisClient'] = None
    _redis: Optional[aioredis.Redis] = None
    _lock = asyncio.Lock()
    _initialized = False
    
    def __new__(cls) -> 'RedisClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def initialize(self) -> None:
        """Initialize Redis connection with retry logic.
        
        Raises:
            redis.RedisError: If connection to Redis fails after retries
        """
        if self._redis is not None and await self._redis.ping():
            return
            
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                self._redis = await aioredis.from_url(
                    str(settings.REDIS_URL),
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=settings.REDIS_POOL_SIZE,
                    socket_connect_timeout=5.0,
                    socket_timeout=5.0,
                    retry_on_timeout=True,
                    retry_on_error=[ConnectionError, TimeoutError],
                )
                await self._redis.ping()
                self._initialized = True
                logger.info("Successfully connected to Redis")
                return
                
            except (aioredis.RedisError, ConnectionError, TimeoutError) as e:
                if attempt == max_retries - 1:
                    logger.error("Failed to connect to Redis after %d attempts: %s", max_retries, e)
                    self._initialized = False
                    raise
                    
                logger.warning(
                    "Redis connection attempt %d/%d failed: %s. Retrying in %ds...",
                    attempt + 1,
                    max_retries,
                    str(e),
                    retry_delay,
                )
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    async def close(self) -> None:
        """Close Redis connection and cleanup resources.
        
        This should be called during application shutdown.
        """
        if self._redis is not None:
            try:
                await self._redis.close()
                await self._redis.connection_pool.disconnect()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error("Error closing Redis connection: %s", e, exc_info=True)
            finally:
                self._redis = None
                self._initialized = False
    
    @overload
    async def get(self, key: str) -> Optional[str]:
        ...
        
    @overload
    async def get(self, key: str, model: type[T]) -> Optional[T]:
        ...
        
    async def get(self, key: str, model: Optional[type[T]] = None) -> Any:
        """Get value by key with optional model deserialization.
        
        Args:
            key: The key to retrieve
            model: Optional Pydantic model to deserialize into
            
        Returns:
            The value if found, None otherwise. If model is provided, returns
            an instance of the model if the value exists and is valid JSON.
        """
        await self._ensure_connected()
        
        value = await self._redis.get(key)
        if value is None:
            return None
            
        if model is not None:
            try:
                data = json.loads(value)
                if issubclass(model, BaseModel):
                    return model.parse_obj(data)
                return model(data)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Failed to deserialize value for key %s: %s", key, e)
                return None
                
        return value
    
    async def set(
        self,
        key: str,
        value: RedisValue,
        expire: Optional[Union[int, float, timedelta]] = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """Set key-value pair with optional expiration and conditions.
        
        Args:
            key: The key to set
            value: The value to store (can be any JSON-serializable object or Pydantic model)
            expire: Expiration time in seconds or as timedelta
            nx: If True, only set the key if it does not already exist
            xx: If True, only set the key if it already exists
            
        Returns:
            bool: True if the operation was successful, False otherwise
            
        Raises:
            ValueError: If both nx and xx are True
        """
        if nx and xx:
            raise ValueError("'nx' and 'xx' cannot both be True")
            
        await self._ensure_connected()
        
        # Convert Pydantic models to dict
        if isinstance(value, BaseModel):
            value = value.dict()
            
        # Serialize non-scalar values to JSON
        if isinstance(value, (dict, list)):
            value = json.dumps(value, default=self._json_serializer)
            
        # Convert timedelta to seconds
        if isinstance(expire, timedelta):
            expire = int(expire.total_seconds())
            
        # Set the key with the appropriate options
        if nx:
            return await self._redis.set(key, value, ex=expire, nx=True)
        elif xx:
            return await self._redis.set(key, value, ex=expire, xx=True)
        else:
            return await self._redis.set(key, value, ex=expire)
            
    @staticmethod
    def _json_serializer(obj: Any) -> Any:
        """Custom JSON serializer for non-standard types."""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
        
    async def _ensure_connected(self) -> None:
        """Ensure Redis connection is established."""
        if self._redis is None or not self._initialized:
            async with self._lock:
                if self._redis is None or not self._initialized:
                    await self.initialize()

    async def expire(self, key: str, time: Union[int, timedelta]) -> bool:
        """Set a key's time to live in seconds.
        
        Args:
            key: The key to set expiration for
            time: Time in seconds or as timedelta
            
        Returns:
            bool: True if the timeout was set, False if key doesn't exist
        """
        if isinstance(time, timedelta):
            time = int(time.total_seconds())
            
        await self._ensure_connected()
        return await self._redis.expire(key, time)
        
    async def ttl(self, key: str) -> Optional[int]:
        """Get the time to live for a key in seconds.
        
        Returns:
            int: TTL in seconds, -2 if key doesn't exist, -1 if key exists but has no TTL
        """
        await self._ensure_connected()
        return await self._redis.ttl(key)
        
    async def keys(self, pattern: str = "*") -> List[str]:
        """Find all keys matching the given pattern.
        
        Warning: This should be used with caution in production as it may be slow
        on large databases.
        """
        await self._ensure_connected()
        return await self._redis.keys(pattern)
        
    async def flushdb(self) -> bool:
        """Delete all keys in the current database.
        
        Warning: This is a destructive operation and should be used with caution.
        """
        await self._ensure_connected()
        return await self._redis.flushdb()
        
    async def ping(self) -> bool:
        """Ping the Redis server."""
        try:
            await self._ensure_connected()
            return await self._redis.ping()
        except (aioredis.RedisError, ConnectionError):
            return False
    
    async def delete(self, *keys: str) -> int:
        """Delete one or more keys.
        
        Args:
            *keys: One or more keys to delete
            
        Returns:
            int: Number of keys that were deleted
        """
        if not keys:
            return 0
            
        await self._ensure_connected()
        return await self._redis.delete(*keys)
    
    async def exists(self, *keys: str) -> int:
        """Check if one or more keys exist.
        
        Args:
            *keys: One or more keys to check
            
        Returns:
            int: Number of keys that exist
        """
        if not keys:
            return 0
            
        await self._ensure_connected()
        return await self._redis.exists(*keys)
    
    async def incr(
        self,
        key: str,
        amount: int = 1,
        maximum: Optional[int] = None,
        expire: Optional[Union[int, timedelta]] = None,
    ) -> int:
        """Increment key by amount with optional maximum value and expiration.
        
        Args:
            key: The key to increment
            amount: Amount to increment by (can be negative)
            maximum: Optional maximum value (inclusive)
            expire: Optional expiration time in seconds or as timedelta
            
        Returns:
            int: The new value after incrementing
            
        Raises:
            ValueError: If the value would exceed the maximum
        """
        await self._ensure_connected()
        
        # Convert timedelta to seconds
        if isinstance(expire, timedelta):
            expire = int(expire.total_seconds())
        
        # Use a Lua script for atomic operation
        lua_script = """
        local current = redis.call('GET', KEYS[1])
        current = tonumber(current) or 0
        
        local new_value = current + tonumber(ARGV[1])
        
        if ARGV[2] ~= '' and new_value > tonumber(ARGV[2]) then
            return redis.error_reply("increment would exceed maximum")
        end
        
        redis.call('SET', KEYS[1], new_value)
        
        if ARGV[3] ~= '' then
            redis.call('EXPIRE', KEYS[1], ARGV[3])
        end
        
        return new_value
        """
        
        try:
            result = await self._redis.eval(
                lua_script,
                1,  # Number of keys
                key,
                amount,
                str(maximum) if maximum is not None else '',
                str(expire) if expire is not None else '',
            )
            return int(result)
            
        except aioredis.ResponseError as e:
            if "would exceed maximum" in str(e):
                raise ValueError("Increment would exceed maximum value") from e
            raise
    
    async def decr(
        self,
        key: str,
        amount: int = 1,
        minimum: Optional[int] = None,
        expire: Optional[Union[int, timedelta]] = None,
    ) -> int:
        """Decrement key by amount with optional minimum value and expiration.
        
        Args:
            key: The key to decrement
            amount: Amount to decrement by (can be negative)
            minimum: Optional minimum value (inclusive)
            expire: Optional expiration time in seconds or as timedelta
            
        Returns:
            int: The new value after decrementing
            
        Raises:
            ValueError: If the value would go below the minimum
        """
        await self._ensure_connected()
        
        # Convert timedelta to seconds
        if isinstance(expire, timedelta):
            expire = int(expire.total_seconds())
        
        # Use a Lua script for atomic operation
        lua_script = """
        local current = redis.call('GET', KEYS[1])
        current = tonumber(current) or 0
        
        local new_value = current - tonumber(ARGV[1])
        
        if ARGV[2] ~= '' and new_value < tonumber(ARGV[2]) then
            return redis.error_reply("decrement would go below minimum")
        end
        
        redis.call('SET', KEYS[1], new_value)
        
        if ARGV[3] ~= '' then
            redis.call('EXPIRE', KEYS[1], ARGV[3])
        end
        
        return new_value
        """
        
        try:
            result = await self._redis.eval(
                lua_script,
                1,  # Number of keys
                key,
                amount,
                str(minimum) if minimum is not None else '',
                str(expire) if expire is not None else '',
            )
            return int(result)
            
        except aioredis.ResponseError as e:
            if "would go below minimum" in str(e):
                raise ValueError("Decrement would go below minimum value") from e
            raise
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        """Get value from hash field.
        
        Args:
            name: Name of the hash
            key: Field name within the hash
            
        Returns:
            The value of the field, or None if it doesn't exist
        """
        await self._ensure_connected()
        return await self._redis.hget(name, key)
        
    async def hgetall(self, name: str) -> Dict[str, str]:
        """Get all fields and values from a hash.
        
        Args:
            name: Name of the hash
            
        Returns:
            Dictionary of all field-value pairs in the hash
        """
        await self._ensure_connected()
        return await self._redis.hgetall(name)
        
    async def hset(
        self,
        name: str,
        key: Optional[str] = None,
        value: Optional[RedisEncodable] = None,
        mapping: Optional[Dict[str, RedisEncodable]] = None,
    ) -> int:
        """Set one or more hash fields.
        
        Args:
            name: Name of the hash
            key: Field name (if setting a single field)
            value: Field value (if setting a single field)
            mapping: Dictionary of field-value pairs to set
            
        Returns:
            int: Number of fields that were added or updated
            
        Raises:
            ValueError: If neither key/value nor mapping is provided
        """
        if (key is None or value is None) and not mapping:
            raise ValueError("Either key/value or mapping must be provided")
            
        await self._ensure_connected()
        
        if mapping is not None:
            # Convert all values to strings
            str_mapping = {}
            for k, v in mapping.items():
                if isinstance(v, (dict, list)):
                    str_mapping[k] = json.dumps(v, default=self._json_serializer)
                else:
                    str_mapping[k] = str(v)
            return await self._redis.hset(name, mapping=str_mapping)
            
        # Handle single key/value pair
        if isinstance(value, (dict, list)):
            value = json.dumps(value, default=self._json_serializer)
        return await self._redis.hset(name, key, value)
    
    async def hgetall(self, name: str) -> Dict[str, str]:
        """Get all key-value pairs from hash."""
        if not self._redis:
            await self.initialize()
        return await self._redis.hgetall(name)
    
    async def hset(self, name: str, key: str, value: Union[str, int, float, bool, Dict, list]) -> int:
        """Set key-value pair in hash."""
        if not self._redis:
            await self.initialize()
            
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self._redis.hset(name, key, value)
    
    async def acquire_lock(self, lock_name: str, expire: int = 60) -> bool:
        """Acquire a distributed lock."""
        if not self._redis:
            await self.initialize()
            
        # Try to set the lock with NX (only if not exists) and EX (expire time)
        return await self._redis.set(lock_name, "1", nx=True, ex=expire)
    
    async def release_lock(self, lock_name: str) -> None:
        """Release a distributed lock."""
        if not self._redis:
            await self.initialize()
        await self._redis.delete(lock_name)
    
    @asynccontextmanager
    async def lock(self, lock_name: str, expire: int = 60):
        """Context manager for distributed lock."""
        acquired = await self.acquire_lock(lock_name, expire)
        try:
            if not acquired:
                raise RuntimeError(f"Could not acquire lock: {lock_name}")
            yield
        finally:
            if acquired:
                await self.release_lock(lock_name)

def with_redis_lock(lock_name: str, expire: int = 60):
    """Decorator for functions that need distributed locking."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = RedisClient()
            async with redis.lock(lock_name, expire):
                return await func(*args, **kwargs)
        return wrapper
    return decorator

# Global Redis client instance
redis = RedisClient()

# Alias for backward compatibility
redis_client = redis

# Clean up on application shutdown
async def close_redis_connection() -> None:
    """Close the Redis connection on application shutdown."""
    await redis.close()

# Register cleanup handler
import atexit
import asyncio

if not settings.TESTING:
    loop = asyncio.get_event_loop()
    atexit.register(lambda: loop.run_until_complete(close_redis_connection()))
