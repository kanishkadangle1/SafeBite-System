import re


SYMPTOM_KEYWORDS = {
    "vomiting": ["vomiting", "vomit", "threw up", "throwing up"],
    "diarrhea": ["diarrhea", "diarrhoea", "loose motion", "loose motions"],
    "stomach pain": ["stomach pain", "stomach ache", "abdominal pain", "cramps"],
    "nausea": ["nausea", "nauseous"],
    "fever": ["fever", "high temperature"],
    "headache": ["headache", "head pain"],
    "food poisoning": ["food poisoning", "foodborne illness"],
}


FOOD_KEYWORDS = [
    "biryani",
    "rice",
    "chicken",
    "paneer",
    "pizza",
    "burger",
    "sandwich",
    "noodles",
    "fish",
    "meat",
    "milk",
    "curd",
    "ice cream",
    "cake",
    "bread",
    "samosa",
    "dosa",
    "idli",
]


PLATFORM_KEYWORDS = {
    "swiggy": "Swiggy",
    "zomato": "Zomato",
    "zepto": "Zepto",
    "blinkit": "Blinkit",
    "uber eats": "Uber Eats",
}


SEVERITY_KEYWORDS = {
    "high": [
        "hospital",
        "hospitalized",
        "hospitalised",
        "severe",
        "blood",
        "fainted",
        "unconscious",
    ],
    "medium": [
        "vomiting",
        "vomit",
        "diarrhea",
        "diarrhoea",
        "fever",
        "dehydration",
    ],
}


def extract_symptoms(text: str) -> list[str]:
    text_lower = text.lower()
    symptoms = []

    for symptom, keywords in SYMPTOM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                symptoms.append(symptom)
                break

    return symptoms


def extract_foods(text: str) -> list[str]:
    text_lower = text.lower()

    return [
        food
        for food in FOOD_KEYWORDS
        if re.search(rf"\b{re.escape(food)}\b", text_lower)
    ]


def extract_platform(text: str) -> str | None:
    text_lower = text.lower()

    for keyword, platform in PLATFORM_KEYWORDS.items():
        if keyword in text_lower:
            return platform

    return None


def extract_people_affected(text: str) -> int | None:
    patterns = [
        r"(\d+)\s+(?:people|persons|of us|members)",
        r"(\d+)\s+(?:people|persons)\s+(?:were|got|became)",
    ]

    text_lower = text.lower()

    for pattern in patterns:
        match = re.search(pattern, text_lower)

        if match:
            return int(match.group(1))

    return None


def calculate_signal_level(
    symptoms: list[str],
    people_affected: int | None,
    text: str,
) -> str:
    text_lower = text.lower()

    if any(
        keyword in text_lower
        for keyword in SEVERITY_KEYWORDS["high"]
    ):
        return "HIGH"

    if people_affected and people_affected >= 3:
        return "HIGH"

    if symptoms:
        return "MEDIUM"

    return "LOW"


def analyze_complaint(text: str) -> dict:
    symptoms = extract_symptoms(text)
    foods = extract_foods(text)
    platform = extract_platform(text)
    people_affected = extract_people_affected(text)

    signal_level = calculate_signal_level(
        symptoms=symptoms,
        people_affected=people_affected,
        text=text,
    )

    return {
        "symptoms": symptoms,
        "foods": foods,
        "platform": platform,
        "people_affected": people_affected,
        "signal_level": signal_level,
    }
