import uuid
from datetime import datetime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from backend.src.shared.database.base import Base
from backend.src.shared.mixins.repr_mixin import ReprMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from backend.src.shared.enum.teacher_application import TeacherApplicationStatus


class TeacherApplicationModel(Base, ReprMixin):
    __tablename__ = "teacher_applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    teaching_since: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    degree: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    field_of_study: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[TeacherApplicationStatus] = mapped_column(
        SQLEnum(
            TeacherApplicationStatus,
            name="teacherapplicationstatus",
            create_type=True
        ),
        nullable=False,
        default=TeacherApplicationStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="teacher_applications"
    )
