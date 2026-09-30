SafeBite System
Food Safety Reporting and Intelligence System

SafeBite is a web-based food safety reporting and intelligence system designed to help users report suspected food safety incidents, track submitted complaints, and provide structured information for authorized review.

The system combines a responsive web interface with a FastAPI backend, SQLite database, and AI-assisted complaint analysis to support complaint classification, risk assessment, prioritization, and SLA monitoring.

Features

Food safety complaint submission

Unique complaint reference number generation

Complaint status tracking

Complaint retrieval by reference number

REST API built with FastAPI

SQLite database for complaint storage

AI-assisted complaint analysis

Risk score generation

Severity classification

Priority classification

Detection of reported symptoms

Detection of serious safety signals

SLA deadline calculation

SLA monitoring

High-risk case identification

Officer dashboard summary

Recent complaint overview

Responsive frontend interface

API documentation through Swagger/OpenAPI

Technology Stack
Frontend

HTML5

CSS3

JavaScript

Responsive CSS layouts

Fetch API for backend communication

Backend

Python

FastAPI

SQLAlchemy

Pydantic

SQLite

Uvicorn

AI / Machine Learning

TensorFlow

AI-assisted complaint analysis

The AI component is intended to provide decision-support and structured risk assessment. It does not replace assessment or decisions made by authorized food safety professionals.

System Architecture
                    ┌──────────────────────┐
                    │      User / Officer  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Web Frontend       │
                    │ HTML / CSS / JS      │
                    └──────────┬───────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ SQLite Database  │       │ AI Analysis      │
       │                  │       │                  │
       │ Complaints       │       │ Risk Score       │
       │ Status           │       │ Severity         │
       │ Priority         │       │ Symptoms         │
       │ SLA Data         │       │ Serious Signals  │
       └──────────────────┘       └─────────┬────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │ Officer          │
                                  │ Dashboard        │
                                  └──────────────────┘

Project Structure
SafeBite System/
│
├── backend/
│   │
│   ├── app/
│   │   ├── database/
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │
│   │   └── main.py
│   │
│   ├── ai/
│   │   └── complaint_analyzer.py
│   │
│   ├── requirements.txt
│   └── safebite.db
│
├── frontend/
│   │
│   ├── css/
│   │   ├── base.css
│   │   ├── public.css
│   │   └── dashboard.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── report.js
│   │   ├── track.js
│   │   ├── case.js
│   │   └── dashboard.js
│   │
│   ├── case.html
│   ├── dashboard.html
│   ├── report.html
│   └── track.html
│
├── .gitignore
└── README.md

Core Workflow
1. Submit a Complaint

A user provides information about a suspected food safety incident, including:

Description of the incident

Business name

Food product

Order channel

Delivery platform, where applicable

Order date

Number of people affected

Reported symptoms

The frontend sends this information to the FastAPI backend.

2. Store the Complaint

The backend validates the request and stores the complaint in the SQLite database.

A unique complaint reference number is associated with the complaint.

3. Track the Complaint

Users can enter their complaint reference number to retrieve the current complaint status.

The tracking interface displays information such as:

Complaint reference number

Business

Food product

Order channel

People affected

Current status

Status message

4. AI-Assisted Analysis

An authorized workflow can send an existing complaint for analysis.

The analysis processes complaint information and produces structured results including:

Risk score

Severity

Detected symptoms

Serious safety signals

Analysis type

5. Priority Assignment

The system maps the AI-assessed severity to an operational priority.

CRITICAL → URGENT
HIGH     → HIGH
MEDIUM   → MEDIUM
LOW      → NORMAL

6. SLA Monitoring

The system assigns an SLA according to severity.

CRITICAL → 4 hours
HIGH     → 8 hours
MEDIUM   → 24 hours
LOW      → 48 hours


The system can identify whether an SLA is:

ON_TRACK
AT_RISK
BREACHED

7. Officer Dashboard

The dashboard API provides summary information including:

Total complaints

AI-analyzed complaints

High-risk cases

SLA breaches

SLA cases at risk

Recent complaints

Complaint priority

Complaint severity

Risk score

Number of people affected

SLA status

API Endpoints
Home
GET /


Returns basic information about the SafeBite API.

Health Check
GET /health


Checks whether the backend service is running.

Create Complaint
POST /complaints


Creates a new food safety complaint.

Get All Complaints
GET /complaints


Returns stored complaints.

Get Single Complaint
GET /complaints/{complaint_number}


Retrieves a complaint using its reference number.

Analyze Complaint
POST /complaints/{complaint_number}/analyze


Runs AI-assisted analysis for an existing complaint.

Dashboard Summary
GET /dashboard/summary


Returns dashboard statistics and recent complaint information.

Running the Backend
1. Navigate to the Backend
cd backend

2. Create a Virtual Environment
python -m venv .venv

3. Activate the Virtual Environment

Windows:

.venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Start the FastAPI Server
uvicorn app.main:app --reload


The API will be available at:

http://127.0.0.1:8000

API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs


ReDoc:

http://127.0.0.1:8000/redoc


These interfaces can be used to test and inspect the available API endpoints.

Frontend

The frontend consists of HTML, CSS, and JavaScript files.

The JavaScript API layer communicates with the FastAPI server using HTTP requests.

The frontend currently uses:

http://127.0.0.1:8000


as the local API base URL.

Before using the frontend, make sure the FastAPI backend is running.

Example Complaint Analysis

A complaint can be analyzed through:

POST /complaints/{complaint_number}/analyze


The system produces structured information similar to:

{
    "risk_score": 75,
    "severity": "HIGH",
    "detected_symptoms": [
        "vomiting",
        "diarrhea"
    ],
    "serious_signals": [],
    "analysis_type": "AI-assisted risk assessment"
}


The exact result depends on the complaint information processed by the analysis system.

Risk and SLA Logic

The system uses severity to determine operational priority and SLA duration.

Severity	Priority	SLA
CRITICAL	URGENT	4 hours
HIGH	HIGH	8 hours
MEDIUM	MEDIUM	24 hours
LOW	NORMAL	48 hours

SLA monitoring then determines whether a case is:

ON_TRACK — sufficient time remains

AT_RISK — one hour or less remains

BREACHED — the SLA deadline has passed

Database

SafeBite currently uses SQLite for local data persistence.

The database stores complaint-related information such as:

Complaint details

Business information

Food product

Order information

People affected

Reported symptoms

Complaint status

AI risk score

AI severity

AI-detected symptoms

Serious safety signals

Priority

SLA deadline

Creation timestamp

Error Handling

The frontend API layer handles common backend errors including:

Server connection failures

HTTP errors

FastAPI validation errors

Complaint not found errors

API response errors

The backend returns appropriate HTTP responses for invalid or missing complaints.

Security and Responsible Use

SafeBite is designed as a prototype/project system for food safety reporting and intelligence.

The AI analysis should be treated as decision-support rather than an autonomous authority.

Final investigation, enforcement, or food safety decisions should remain with authorized personnel.

For deployment beyond local development, additional security measures should be implemented, including:

Authentication and authorization

HTTPS

Secure environment variables

Database security

Input validation

Rate limiting

Production logging

Access control

Secure API configuration

Current Development Status

The current system includes the core complaint reporting, tracking, backend API, database, AI-assisted analysis, risk assessment, SLA monitoring, and dashboard API functionality.

The project is structured so that additional machine learning models, authentication, production deployment, and advanced dashboard features can be added in future versions.

Future Enhancements

Potential future improvements include:

Officer authentication

Role-based access control

Advanced dashboard visualizations

Geographic incident mapping

Complaint trend analysis

Automated notifications

More advanced machine learning models

Model training using validated historical complaint data

Production database deployment

Cloud hosting

Audit logging

Automated report generation

Project Purpose

SafeBite aims to provide a structured digital workflow for food safety complaint reporting and review.

The system connects public reporting with backend data management and AI-assisted analysis so that complaint information can be organized, prioritized, tracked, and reviewed through a centralized system.

Disclaimer

SafeBite is an academic/project implementation.

AI-generated analysis, risk scores, classifications, and priorities should not be treated as a replacement for professional food safety assessment or official regulatory decisions.
