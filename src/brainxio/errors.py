class BrainXioError(Exception):
    """Base exception for BrainXio errors."""
    pass

class LoggingError(BrainXioError):
    """Exception for logging setup failures."""
    pass

class CacheError(BrainXioError):
    """Exception for cache operation failures."""
    pass

class ConfigError(BrainXioError):
    """Exception for configuration operation failures."""
    pass
