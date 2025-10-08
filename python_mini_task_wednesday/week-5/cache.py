import json
import logging
import os
from typing import Any, Optional

import redis
from redis.exceptions import ConnectionError, RedisError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheService:
    """
    Redis-based cache service for the Task Management API.

    Provides methods for caching, retrieving, and invalidating cached data
    with proper error handling and logging.
    """

    def __init__(self):
        """Initialize the Redis cache service with configuration."""
        self.redis_client = None
        self.cache_enabled = self._get_bool_config("CACHE_ENABLED", True)
        self.default_ttl = int(os.getenv("CACHE_DEFAULT_TTL", 300))  # 5 minutes
        self.task_ttl = int(os.getenv("CACHE_TASK_TTL", 600))  # 10 minutes
        self.subtask_ttl = int(os.getenv("CACHE_SUBTASK_TTL", 300))  # 5 minutes

        if self.cache_enabled:
            self._connect_redis()

    def _get_bool_config(self, key: str, default: bool) -> bool:
        """Convert environment variable to boolean."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    def _connect_redis(self):
        """Establish Redis connection with error handling."""
        try:
            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = int(os.getenv("REDIS_PORT", 6379))
            redis_password = os.getenv("REDIS_PASSWORD")
            redis_db = int(os.getenv("REDIS_DB", 0))

            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
            )

            # Test connection
            self.redis_client.ping()
            logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")

        except ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.cache_enabled = False
            self.redis_client = None
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            self.cache_enabled = False
            self.redis_client = None

    def _is_connected(self) -> bool:
        """Check if Redis connection is available."""
        if not self.cache_enabled or not self.redis_client:
            return False

        try:
            self.redis_client.ping()
            return True
        except (ConnectionError, RedisError):
            logger.warning("Redis connection lost, attempting to reconnect...")
            self._connect_redis()
            return self.redis_client is not None

    def get_from_cache(self, key: str) -> Optional[Any]:
        """
        Retrieve data from cache.

        Args:
            key: Cache key

        Returns:
            Cached data if found, None otherwise
        """
        if not self._is_connected():
            logger.debug(f"Cache miss (not connected): {key}")
            return None

        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                logger.info(f"Cache hit: {key}")
                return json.loads(cached_data)
            else:
                logger.info(f"Cache miss: {key}")
                return None
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error retrieving from cache {key}: {e}")
            return None

    def set_in_cache(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        """
        Store data in cache.

        Args:
            key: Cache key
            value: Data to cache
            expiry: TTL in seconds (uses default if None)

        Returns:
            True if successful, False otherwise
        """
        if not self._is_connected():
            logger.debug(f"Cache set failed (not connected): {key}")
            return False

        try:
            if expiry is None:
                expiry = self.default_ttl

            serialized_value = json.dumps(value, default=str)
            result = self.redis_client.setex(key, expiry, serialized_value)

            if result:
                logger.info(f"Cache set: {key} (TTL: {expiry}s)")
                return True
            else:
                logger.warning(f"Failed to set cache: {key}")
                return False

        except (RedisError, TypeError) as e:
            logger.error(f"Error setting cache {key}: {e}")
            return False

    def delete_from_cache(self, key: str) -> bool:
        """
        Delete data from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        if not self._is_connected():
            logger.debug(f"Cache delete failed (not connected): {key}")
            return False

        try:
            result = self.redis_client.delete(key)
            if result:
                logger.info(f"Cache deleted: {key}")
                return True
            else:
                logger.info(f"Cache key not found for deletion: {key}")
                return True  # Key not existing is considered success

        except RedisError as e:
            logger.error(f"Error deleting from cache {key}: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.

        Args:
            pattern: Redis key pattern (e.g., "task:*")

        Returns:
            Number of keys deleted
        """
        if not self._is_connected():
            logger.debug(f"Cache pattern delete failed (not connected): {pattern}")
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted_count = self.redis_client.delete(*keys)
                logger.info(
                    f"Deleted {deleted_count} cache keys matching pattern: {pattern}"
                )
                return deleted_count
            else:
                logger.info(f"No cache keys found matching pattern: {pattern}")
                return 0

        except RedisError as e:
            logger.error(f"Error deleting cache pattern {pattern}: {e}")
            return 0

    def invalidate_task_cache(self, task_id: int) -> bool:
        """
        Invalidate all cache entries related to a specific task.

        Args:
            task_id: ID of the task to invalidate

        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete individual task cache
            task_key = f"task:{task_id}"
            self.delete_from_cache(task_key)

            # Delete task subtasks cache
            subtasks_key = f"task:{task_id}:subtasks"
            self.delete_from_cache(subtasks_key)

            logger.info(f"Invalidated cache for task {task_id}")
            return True

        except Exception as e:
            logger.error(f"Error invalidating task cache for task {task_id}: {e}")
            return False

    def invalidate_subtask_cache(
        self, subtask_id: int, task_id: Optional[int] = None
    ) -> bool:
        """
        Invalidate cache entries related to a specific subtask.

        Args:
            subtask_id: ID of the subtask to invalidate
            task_id: Optional parent task ID for additional invalidation

        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete individual subtask cache
            subtask_key = f"subtask:{subtask_id}"
            self.delete_from_cache(subtask_key)

            # If task_id is provided, also invalidate parent task cache
            if task_id:
                self.invalidate_task_cache(task_id)

            logger.info(f"Invalidated cache for subtask {subtask_id}")
            return True

        except Exception as e:
            logger.error(
                f"Error invalidating subtask cache for subtask {subtask_id}: {e}"
            )
            return False

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self._is_connected():
            return {"status": "disconnected", "cache_enabled": self.cache_enabled}

        try:
            info = self.redis_client.info()
            return {
                "status": "connected",
                "cache_enabled": self.cache_enabled,
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
            }
        except RedisError as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"status": "error", "error": str(e)}


# Global cache service instance
cache_service = CacheService()


# Cache key generation utilities
def get_task_cache_key(task_id: int) -> str:
    """Generate cache key for individual task."""
    return f"task:{task_id}"


def get_subtask_cache_key(subtask_id: int) -> str:
    """Generate cache key for individual subtask."""
    return f"subtask:{subtask_id}"


def get_task_subtasks_cache_key(task_id: int) -> str:
    """Generate cache key for task's subtasks list."""
    return f"task:{task_id}:subtasks"


def get_tasks_list_cache_key() -> str:
    """Generate cache key for all tasks list."""
    return "tasks:all"
