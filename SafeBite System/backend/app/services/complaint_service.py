from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.complaint import Complaint


def generate_complaint_number(db: Session) -> str:
    year = datetime.now().year

    count = (
        db.query(func.count(Complaint.id))
        .filter(
            Complaint.complaint_number.like(f"SB-{year}-%")
        )
        .scalar()
    )

    next_number = (count or 0) + 1

    return f"SB-{year}-{next_number:06d}"
