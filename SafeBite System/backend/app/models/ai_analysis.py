from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        unique=True,
        nullable=False,
    )

    extracted_symptoms: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    extracted_foods: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    detected_platform: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    detected_people_affected: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    signal_level: Mapped[str] = mapped_column(
        String(20),
        default="LOW",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
