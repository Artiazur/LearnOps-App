from backend.src.core.exceptions.base import RedisError

class RedisUnavailableError(RedisError):
    """Raised when Redis is unavailable."""
    
    pass