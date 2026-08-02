class ReprMixin:
    repr_exclude = {"password", "hashed_password"}

    def __repr__(self):
        attribute = []

        for column in self.__table__.columns:
            name = column.name
            if name in self.repr_exclude:
                value = "***"
            else:
                value = getattr(self, name)

            attribute.append(f"{name}={value!r}")

        return f"<{self.__class__.__name__}({', '.join(attribute)})>"