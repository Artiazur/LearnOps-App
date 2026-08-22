# Provides a reusable representation for SQLAlchemy models.
#
# This mixin centralizes model representation logic so individual ORM models
# do not need to implement their own __repr__ methods. It also prevents
# sensitive attributes from being exposed when model instances are printed
# or included in logs.

class ReprMixin:
    """Provides a consistent and safe string representation for ORM models.

    The representation is generated from the model's database columns and
    masks attributes listed in ``repr_exclude`` to reduce the risk of exposing
    sensitive data during debugging or logging.
    """

    repr_exclude = {"password", "hashed_password"}

    def __repr__(self):
        """Return a readable representation of the model instance.

        Database column values are included for debugging purposes, while
        sensitive attributes configured in ``repr_exclude`` are masked.
        """

        attribute = []

        for column in self.__table__.columns:
            name = column.name

            if name in self.repr_exclude:
                value = "***"
            else:
                value = getattr(self, name)

            attribute.append(f"{name}={value!r}")

        return f"<{self.__class__.__name__}({', '.join(attribute)})>"