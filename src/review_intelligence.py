import re
import string
from pathlib import Path

import joblib


# ---------------------------------------------------------
# 1. Locate and load the trained machine-learning artifacts
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "sentiment_model.joblib"
VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.joblib"

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)


# ---------------------------------------------------------
# 2. Text cleaning
# Must match the cleaning used during model training
# ---------------------------------------------------------

def clean_text(text):
    text = str(text).lower()
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ---------------------------------------------------------
# 3. Hotel complaint categories
# ---------------------------------------------------------

COMPLAINT_CATEGORIES = {
    "Cleanliness": [
        "dirty",
        "filthy",
        "smell",
        "smelly",
        "unclean",
        "cleanliness",
        "stain",
        "dust",
        "mold"
    ],

    "Room": [
        "room",
        "small",
        "broken",
        "old",
        "air conditioning",
        "aircondition",
        "ac",
        "heating"
    ],

    "Staff / Service": [
        "staff",
        "service",
        "reception",
        "desk",
        "rude",
        "unfriendly",
        "helpful",
        "manager"
    ],

    "Food / Breakfast": [
        "food",
        "breakfast",
        "restaurant",
        "meal",
        "dinner",
        "lunch"
    ],

    "Bed / Bathroom": [
        "bed",
        "bathroom",
        "shower",
        "toilet",
        "towel",
        "mattress"
    ],

    "Price / Value": [
        "price",
        "expensive",
        "overpriced",
        "value",
        "cheap",
        "money"
    ],

    "Noise": [
        "noise",
        "noisy",
        "loud",
        "sound"
    ],

    "Wi-Fi / Internet": [
        "wifi",
        "wi-fi",
        "internet",
        "connection"
    ],

    "Parking": [
        "parking",
        "car park",
        "garage"
    ]
}


# ---------------------------------------------------------
# 4. Hotel departments responsible for each complaint type
# ---------------------------------------------------------

DEPARTMENTS = {
    "Cleanliness": "Housekeeping",
    "Room": "Rooms Division / Maintenance",
    "Staff / Service": "Front Office / Guest Relations",
    "Food / Breakfast": "Food & Beverage",
    "Bed / Bathroom": "Housekeeping / Maintenance",
    "Price / Value": "Revenue Management / Front Office",
    "Noise": "Front Office / Security",
    "Wi-Fi / Internet": "IT / Engineering",
    "Parking": "Front Office / Operations",
    "General Complaint": "Guest Relations"
}


# ---------------------------------------------------------
# 5. Recommended hotel-management actions
# ---------------------------------------------------------

RECOMMENDED_ACTIONS = {
    "Cleanliness":
        "Arrange an immediate room inspection and corrective cleaning. "
        "Contact the guest and consider a service-recovery gesture.",

    "Room":
        "Inspect the room condition and reported facilities. "
        "Create a maintenance task and consider relocating the guest if necessary.",

    "Staff / Service":
        "Review the service incident with the relevant team. "
        "Contact the guest, acknowledge the experience and provide service recovery.",

    "Food / Breakfast":
        "Notify the Food & Beverage team and investigate the reported issue. "
        "Review food quality, availability and service standards.",

    "Bed / Bathroom":
        "Request immediate Housekeeping or Maintenance inspection. "
        "Resolve the physical room issue and follow up with the guest.",

    "Price / Value":
        "Review the guest's rate, charges and value perception. "
        "Check for billing issues and explain pricing where appropriate.",

    "Noise":
        "Investigate the source of noise and take corrective operational action. "
        "Consider room relocation when necessary.",

    "Wi-Fi / Internet":
        "Notify IT or Engineering to check connectivity. "
        "Provide the guest with an alternative connection or technical assistance.",

    "Parking":
        "Review parking availability, charges and guest instructions. "
        "Provide clear alternatives where possible.",

    "General Complaint":
        "Escalate the review to Guest Relations for manual assessment and follow-up."
}


# ---------------------------------------------------------
# 6. Detect complaint category
# ---------------------------------------------------------

def detect_complaint_category(text):

    cleaned = clean_text(text)

    category_scores = {}

    for category, keywords in COMPLAINT_CATEGORIES.items():

        score = 0

        for keyword in keywords:
            if keyword in cleaned:
                score += 1

        category_scores[category] = score

    best_category = max(
        category_scores,
        key=category_scores.get
    )

    if category_scores[best_category] == 0:
        return "General Complaint"

    return best_category


# ---------------------------------------------------------
# 7. Determine operational priority
# ---------------------------------------------------------

def determine_priority(sentiment, confidence):

    if sentiment == "Negative":

        if confidence >= 0.85:
            return "High"

        return "Medium"

    if sentiment == "Neutral":
        return "Medium"

    return "Low"


# ---------------------------------------------------------
# 8. Complete hotel review analysis
# ---------------------------------------------------------

def analyze_review(review):

    cleaned_review = clean_text(review)

    review_vector = tfidf.transform(
        [cleaned_review]
    )

    sentiment = model.predict(
        review_vector
    )[0]

    probabilities = model.predict_proba(
        review_vector
    )[0]

    confidence = float(
        probabilities.max()
    )

    if sentiment == "Negative":

        complaint_category = detect_complaint_category(
            review
        )

        department = DEPARTMENTS[
            complaint_category
        ]

        recommended_action = RECOMMENDED_ACTIONS[
            complaint_category
        ]

    else:

        complaint_category = "No Critical Complaint Detected"

        department = "Guest Experience"

        recommended_action = (
            "Record the feedback for guest-experience monitoring. "
            "No urgent operational escalation is required."
        )

    priority = determine_priority(
        sentiment,
        confidence
    )

    return {
        "sentiment": sentiment,
        "confidence": round(confidence * 100, 1),
        "complaint_category": complaint_category,
        "department": department,
        "priority": priority,
        "recommended_action": recommended_action
    }


# ---------------------------------------------------------
# 9. Simple local test
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_review = (
        "The bathroom was filthy and the room smelled terrible."
    )

    result = analyze_review(sample_review)

    print(result)
