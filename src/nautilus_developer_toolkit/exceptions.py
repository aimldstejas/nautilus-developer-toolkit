"""
Project-specific exception hierarchy for Nautilus Developer Toolkit.
"""


class NDTError(Exception):
    """Base exception for all Nautilus Developer Toolkit errors."""


class ConfigurationError(NDTError):
    """Configuration-related errors."""


class ValidationError(NDTError):
    """Input validation errors."""


class ServiceError(NDTError):
    """Base class for service-related errors."""


class IntegrationError(NDTError):
    """Base class for external integration errors."""
