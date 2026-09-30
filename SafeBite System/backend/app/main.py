import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ai.complaint_analyzer import analyze_complaint


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="SafeBite System",
    description="Food safety reporting and intelligence API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# SLA CONFIGURATION
# =========================================================

SLA_HOURS = {
    "CRITICAL": 4,
    "HIGH": 8,
    "MEDIUM": 24,
    "LOW": 48
}


# =========================================================
# HOME
# =========================================================

@app.get("/")
def root():

    return {
        "application": "SafeBite System",
        "message": "Food safety reporting and intelligence API",
        "status": "running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "SafeBite API"
    }


# =========================================================
# CREATE COMPLAINT
# =========================================================

@app.post("/complaints")
def create_complaint(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db)
):

    complaint = Complaint(
        description=complaint_data.description,
        business_name=complaint_data.business_name,
        food_product=complaint_data.food_product,
        order_channel=complaint_data.order_channel,
        platform=complaint_data.platform,
        order_date=complaint_data.order_date,
        people_affected=complaint_data.people_affected,
        reported_symptoms=complaint_data.reported_symptoms
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


# =========================================================
# GET ALL COMPLAINTS
# =========================================================

@app.get("/complaints")
def get_complaints(
    db: Session = Depends(get_db)
):

    complaints = (
        db.query(Complaint)
        .order_by(
            Complaint.created_at.desc()
        )
        .all()
    )

    return {
        "count": len(complaints),
        "complaints": complaints
    }


# =========================================================
# GET SINGLE COMPLAINT
# =========================================================

@app.get("/complaints/{complaint_number}")
def get_complaint(
    complaint_number: str,
    db: Session = Depends(get_db)
):

    complaint = (
        db.query(Complaint)
        .filter(
            Complaint.complaint_number
            == complaint_number
        )
        .first()
    )

    if not complaint:

        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return complaint


# =========================================================
# AI COMPLAINT ANALYSIS
# =========================================================

@app.post(
    "/complaints/{complaint_number}/analyze"
)
def analyze_existing_complaint(
    complaint_number: str,
    db: Session = Depends(get_db)
):

    complaint = (
        db.query(Complaint)
        .filter(
            Complaint.complaint_number
            == complaint_number
        )
        .first()
    )

    if not complaint:

        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )


    # -----------------------------------------------------
    # PREPARE TEXT
    # -----------------------------------------------------

    description = (
        str(complaint.description)
        if complaint.description
        else ""
    )

    food_product = (
        str(complaint.food_product)
        if complaint.food_product
        else ""
    )

    business_name = (
        str(complaint.business_name)
        if complaint.business_name
        else ""
    )

    reported_symptoms = (
        str(complaint.reported_symptoms)
        if complaint.reported_symptoms
        else ""
    )


    analysis_text = " ".join(
        value
        for value in [
            description,
            food_product,
            business_name,
            reported_symptoms
        ]
        if value.strip()
    )


    # -----------------------------------------------------
    # RUN AI
    # -----------------------------------------------------

    analysis = analyze_complaint(
        analysis_text
    )


    # -----------------------------------------------------
    # SAVE AI RESULTS
    # -----------------------------------------------------

    complaint.ai_risk_score = int(
        analysis.get(
            "risk_score",
            0
        )
    )

    complaint.ai_severity = str(
        analysis.get(
            "severity",
            "LOW"
        )
    )

    complaint.ai_detected_symptoms = json.dumps(
        analysis.get(
            "detected_symptoms",
            []
        )
    )

    complaint.ai_serious_signals = json.dumps(
        analysis.get(
            "serious_signals",
            []
        )
    )

    complaint.ai_analysis_type = str(
        analysis.get(
            "analysis_type",
            "AI-assisted risk assessment"
        )
    )


    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    severity = analysis.get(
        "severity",
        "LOW"
    )

    if severity == "CRITICAL":

        complaint.priority = "URGENT"

    elif severity == "HIGH":

        complaint.priority = "HIGH"

    elif severity == "MEDIUM":

        complaint.priority = "MEDIUM"

    else:

        complaint.priority = "NORMAL"


    # -----------------------------------------------------
    # SLA
    # -----------------------------------------------------

    sla_hours = SLA_HOURS.get(
        severity,
        48
    )

    created_time = (
        complaint.created_at
        or datetime.utcnow()
    )

    complaint.sla_deadline = (
        created_time
        + timedelta(hours=sla_hours)
    )


    complaint.status = "AI_ANALYZED"


    db.commit()
    db.refresh(complaint)


    # -----------------------------------------------------
    # SLA STATUS
    # -----------------------------------------------------

    now = datetime.utcnow()

    remaining_seconds = (
        complaint.sla_deadline - now
    ).total_seconds()

    if remaining_seconds <= 0:

        sla_status = "BREACHED"

    elif remaining_seconds <= 3600:

        sla_status = "AT_RISK"

    else:

        sla_status = "ON_TRACK"


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "message":
            "Complaint analyzed successfully",

        "complaint_number":
            complaint.complaint_number,

        "status":
            complaint.status,

        "priority":
            complaint.priority,

        "analysis": {

            "risk_score":
                complaint.ai_risk_score,

            "severity":
                complaint.ai_severity,

            "detected_symptoms":
                analysis.get(
                    "detected_symptoms",
                    []
                ),

            "serious_signals":
                analysis.get(
                    "serious_signals",
                    []
                ),

            "analysis_type":
                complaint.ai_analysis_type
        },

        "sla": {

            "allowed_hours":
                sla_hours,

            "deadline":
                complaint.sla_deadline.isoformat(),

            "status":
                sla_status,

            "remaining_hours":
                round(
                    max(
                        remaining_seconds,
                        0
                    ) / 3600,
                    2
                )
        }
    }


# =========================================================
# OFFICER DASHBOARD
# =========================================================

@app.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    complaints = (
        db.query(Complaint)
        .order_by(
            Complaint.created_at.desc()
        )
        .all()
    )


    total = len(complaints)


    high_risk = sum(
        1
        for complaint in complaints
        if complaint.priority
        in ["HIGH", "URGENT"]
    )


    analyzed = sum(
        1
        for complaint in complaints
        if complaint.status
        == "AI_ANALYZED"
    )


    sla_breached = 0
    sla_at_risk = 0


    now = datetime.utcnow()


    for complaint in complaints:

        if not complaint.sla_deadline:
            continue


        remaining = (
            complaint.sla_deadline - now
        ).total_seconds()


        if remaining <= 0:

            sla_breached += 1

        elif remaining <= 3600:

            sla_at_risk += 1


    recent_cases = []


    for complaint in complaints[:10]:

        remaining_hours = None
        sla_status = "NOT_SET"


        if complaint.sla_deadline:

            remaining_seconds = (
                complaint.sla_deadline - now
            ).total_seconds()


            remaining_hours = round(
                max(
                    remaining_seconds,
                    0
                ) / 3600,
                2
            )


            if remaining_seconds <= 0:

                sla_status = "BREACHED"

            elif remaining_seconds <= 3600:

                sla_status = "AT_RISK"

            else:

                sla_status = "ON_TRACK"


        recent_cases.append({

            "complaint_number":
                complaint.complaint_number,

            "business_name":
                complaint.business_name,

            "food_product":
                complaint.food_product,

            "priority":
                complaint.priority,

            "severity":
                complaint.ai_severity,

            "risk_score":
                complaint.ai_risk_score,

            "status":
                complaint.status,

            "people_affected":
                complaint.people_affected,

            "created_at":
                complaint.created_at,

            "sla_deadline":
                complaint.sla_deadline,

            "sla_status":
                sla_status,

            "remaining_hours":
                remaining_hours
        })


    return {

        "dashboard": {

            "total_complaints":
                total,

            "ai_analyzed":
                analyzed,

            "high_risk_cases":
                high_risk,

            "sla_breached":
                sla_breached,

            "sla_at_risk":
                sla_at_risk
        },

        "recent_cases":
            recent_cases
    }
