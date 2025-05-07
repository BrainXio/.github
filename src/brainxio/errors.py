class BrainXioError(Exception):
    """Base exception for BrainXio errors."""
    pass

class LoggingError(BrainXioError):
    """Exception for logging setup failures."""
    pass
