import os

# Configuration module for Redis cache settings


class RedisConfig:
    """Configuration class for Redis connection parameters."""

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.password = os.getenv("REDIS_PASSWORD")
        self.db = int(os.getenv("REDIS_DB", 0))
        self.cache_enabled = self._get_bool_config("CACHE_ENABLED", True)

        # TTL configurations (in seconds)
        self.default_ttl = int(os.getenv("CACHE_DEFAULT_TTL", 300))  # 5 minutes
        self.task_ttl = int(os.getenv("CACHE_TASK_TTL", 600))  # 10 minutes
        self.subtask_ttl = int(os.getenv("CACHE_SUBTASK_TTL", 300))  # 5 minutes
        self.tasks_list_ttl = int(os.getenv("CACHE_TASKS_LIST_TTL", 180))  # 3 minutes

    def _get_bool_config(self, key: str, default: bool) -> bool:
        """Convert environment variable to boolean."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    def to_dict(self) -> dict:
        """Return configuration as dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "db": self.db,
            "cache_enabled": self.cache_enabled,
            "default_ttl": self.default_ttl,
            "task_ttl": self.task_ttl,
            "subtask_ttl": self.subtask_ttl,
            "tasks_list_ttl": self.tasks_list_ttl,
        }


# Global configuration instance
redis_config = RedisConfig()
