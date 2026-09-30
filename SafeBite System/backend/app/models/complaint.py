from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database.database import Base


class Complaint(Base):

    __tablename__ = "complaints"

    # =====================================================
    # IDENTIFICATION
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    complaint_number = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    # =====================================================
    # COMPLAINT INFORMATION
    # =====================================================

    description = Column(
        Text,
        nullable=False
    )

    business_name = Column(
        String,
        nullable=True
    )

    food_product = Column(
        String,
        nullable=True
    )

    # =====================================================
    # ORDER INFORMATION
    # =====================================================

    order_channel = Column(
        String,
        nullable=True
    )

    platform = Column(
        String,
        nullable=True
    )

    order_date = Column(
        String,
        nullable=True
    )

    # =====================================================
    # AFFECTED PEOPLE
    # =====================================================

    people_affected = Column(
        Integer,
        default=0
    )

    # IMPORTANT:
    # Keep this as Text so existing database values
    # are never automatically passed through JSON.loads().
    reported_symptoms = Column(
        Text,
        nullable=True
    )

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    ai_risk_score = Column(
        Integer,
        nullable=True
    )

    ai_severity = Column(
        String,
        nullable=True
    )

    ai_detected_symptoms = Column(
        Text,
        nullable=True
    )

    ai_serious_signals = Column(
        Text,
        nullable=True
    )

    ai_analysis_type = Column(
        String,
        nullable=True
    )

    # =====================================================
    # WORKFLOW
    # =====================================================

    status = Column(
        String,
        default="RECEIVED"
    )

    priority = Column(
        String,
        default="NORMAL"
    )

    # =====================================================
    # SLA
    # =====================================================

    sla_deadline = Column(
        DateTime,
        nullable=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
