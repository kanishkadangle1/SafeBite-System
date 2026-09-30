import re


SYMPTOM_KEYWORDS = {
    "vomiting": [
        "vomiting",
        "vomit",
        "threw up",
        "throwing up"
    ],
    "diarrhea": [
        "diarrhea",
        "diarrhoea",
        "loose motion",
        "loose motions"
    ],
    "stomach pain": [
        "stomach pain",
        "abdominal pain",
        "stomach ache",
        "abdominal cramps",
        "stomach cramps"
    ],
    "nausea": [
        "nausea",
        "nauseous"
    ],
    "fever": [
        "fever",
        "high temperature"
    ],
    "dizziness": [
        "dizziness",
        "dizzy"
    ],
    "headache": [
        "headache",
        "head pain"
    ],
    "weakness": [
        "weakness",
        "very weak",
        "feeling weak"
    ]
}


SERIOUS_KEYWORDS = [
    "blood",
    "hospital",
    "hospitalized",
    "hospitalised",
    "fainted",
    "unconscious",
    "severe",
    "emergency",
    "difficulty breathing",
    "dehydration"
]


def extract_symptoms(text: str) -> list:

    text_lower = text.lower()

    detected_symptoms = []

    for symptom, keywords in SYMPTOM_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text_lower:

                detected_symptoms.append(symptom)

                break

    return list(
        dict.fromkeys(detected_symptoms)
    )


def extract_people_affected(text: str):

    text_lower = text.lower()

    patterns = [

        r"\b(\d+)\s+(?:people|persons|customers|members)\b",

        r"\b(\d+)\s+people\s+ate\b",

        r"\b(\d+)\s+(?:of us|of them)\b",

        r"\b(?:affecting|affected)\s+(\d+)\s+(?:people|persons|customers)\b",

        r"\b(\d+)\s+(?:people|persons|customers)\s+(?:were|are)\s+affected\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            return int(
                match.group(1)
            )

    return None


def extract_serious_signals(text: str) -> list:

    text_lower = text.lower()

    signals = []

    for keyword in SERIOUS_KEYWORDS:

        if keyword in text_lower:

            signals.append(keyword)

    return list(
        dict.fromkeys(signals)
    )


def calculate_risk_score(
    symptoms: list,
    people_affected,
    serious_signals: list
) -> int:

    risk_score = 0

    # -----------------------------------------
    # SYMPTOM SCORE
    # -----------------------------------------

    risk_score += len(symptoms) * 15


    # -----------------------------------------
    # PEOPLE AFFECTED SCORE
    # -----------------------------------------

    if people_affected is not None:

        if people_affected >= 10:

            risk_score += 50

        elif people_affected >= 5:

            risk_score += 35

        elif people_affected >= 3:

            risk_score += 25

        elif people_affected >= 2:

            risk_score += 15

        elif people_affected >= 1:

            risk_score += 5


    # -----------------------------------------
    # SERIOUS SIGNAL SCORE
    # -----------------------------------------

    risk_score += (
        len(serious_signals) * 20
    )


    return min(
        risk_score,
        100
    )


def classify_severity(
    risk_score: int
) -> str:

    if risk_score >= 70:

        return "CRITICAL"

    if risk_score >= 45:

        return "HIGH"

    if risk_score >= 20:

        return "MEDIUM"

    return "LOW"


def analyze_complaint(
    text: str
) -> dict:

    if not text or not text.strip():

        return {
            "detected_symptoms": [],
            "people_affected": None,
            "serious_signals": [],
            "risk_score": 0,
            "severity": "LOW",
            "analysis_type":
                "AI-assisted rule-based risk assessment"
        }


    symptoms = extract_symptoms(
        text
    )


    people_affected = extract_people_affected(
        text
    )


    serious_signals = extract_serious_signals(
        text
    )


    risk_score = calculate_risk_score(
        symptoms=symptoms,
        people_affected=people_affected,
        serious_signals=serious_signals
    )


    severity = classify_severity(
        risk_score
    )


    return {

        "detected_symptoms":
            symptoms,

        "people_affected":
            people_affected,

        "serious_signals":
            serious_signals,

        "risk_score":
            risk_score,

        "severity":
            severity,

        "analysis_type":
            "AI-assisted rule-based risk assessment"
    }


if __name__ == "__main__":

    example = """
    Three people ate chicken biryani.
    Two people started vomiting and had severe
    stomach pain after eating.
    """

    result = analyze_complaint(
        example
    )

    print(result)
