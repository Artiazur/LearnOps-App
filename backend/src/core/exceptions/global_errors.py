# Defines application-wide exceptions that inherit from the shared global
# error category.
#
# These exceptions represent errors that are not specific to a particular
# feature or business operation and can be handled consistently at the
# application boundary.

from backend.src.core.exceptions.base import GlobalError


class SomethingWentWrong(GlobalError):
    """Represents a generic application-level failure.

    The optional message allows the code raising the exception to provide
    additional context while keeping the exception independent from any
    framework-specific HTTP representation.
    """

    def __init__(self, message: str | None = None):
        """Initialize the exception with an optional descriptive message."""

        self.message = message