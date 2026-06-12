"""Exception hierarchy for fortune-telling-core."""


class FortuneTellingError(Exception):
    """Base error for this package."""


class ValidationError(FortuneTellingError, ValueError):
    """Raised when a value object is internally inconsistent."""


class SchemaVersionError(FortuneTellingError):
    """Raised when serialized data uses an unsupported schema version."""


class ExhaustedRngError(FortuneTellingError):
    """Raised when a replay RNG has no remaining values."""


class UnknownSymbolError(FortuneTellingError, LookupError):
    """Raised when a recorded draw references symbols outside the active deck."""
