# Week 5 Task: Adding Redis Cache Service to the Task Management API

## Background

Your Task Management API is functioning well, but as the number of tasks and users grows, database operations are becoming more frequent. To improve performance and reduce the load on your SQLite database, you need to implement a caching layer using Redis.

## Objective

Implement a Redis-based cache service for the Task Management API to improve API response times and reduce database load.

## Requirements

1. **Redis Integration**:
   - Set up a Redis connection using a library like `redis-py`
   - Implement proper error handling for Redis connection failures
   - Configure reasonable expiration times for cached data

2. **Cache Implementation**:
   - Create a cache service module (`cache.py`) that handles all Redis operations
   - Implement the following cache operations:
     - `get_from_cache(key)`
     - `set_in_cache(key, value, expiry=None)`
     - `delete_from_cache(key)`

3. **API Endpoint Caching**:
   - Cache responses for the following read operations:
     - `GET /tasks/{task_id}` - Cache individual tasks by ID
     - `GET /tasks/{task_id}/subtasks` - Cache subtasks for a specific task
     - `GET /subtasks/{subtask_id}` - Cache individual subtask by ID

4. **Cache Invalidation**:
   - Implement cache invalidation when data is modified:
     - When a task is updated, invalidate the specific task cache
     - When a task is deleted, invalidate the specific task cache
     - When a subtask is added/updated/deleted, invalidate:
       - The parent task cache
       - The specific subtask cache (if applicable)
       - The task's subtasks list cache

5. **Cache Key Strategy**:
   - Design a consistent and clear key naming strategy (e.g., `tasks:all`, `task:{task_id}`, `task:{task_id}:subtasks`, `subtask:{subtask_id}`)

6. **Configuration**:
   - Make Redis connection parameters configurable (host, port, password, database)
   - Allow toggling cache functionality on/off through configuration
   - Set appropriate TTL (Time To Live) values for different types of cached data

7. **Monitoring & Logging**:
   - Implement basic logging for cache hits, misses, and errors

8. **Documentation**:
   - Update the README.md to include information about the cache service
   - Document the cache key strategy and expiration policies
   - Provide instructions for setting up Redis locally for development

## Deliverables

1. New `cache.py` module with the Redis cache service implementation
2. Modified API endpoints in `routers.py` to utilize the cache service
3. Updated configuration to include Redis connection parameters
4. Updated README.md with information about the caching implementation

## Further learnings

1. Terminologies used in Cache
2. Cache strategies (currently we implemented 'Read through')
3. Cache Eviction policies
4. Cache Invalidation (currently we implemented 'TTL', and 'Write invalidate')