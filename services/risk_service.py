HIGH_RISK_KEYWORDS = {
    "safety concern": "Potential patient safety issue detected.",
    "adverse event": "Adverse event reporting required.",
    "serious adverse event": "Serious adverse event identified.",
    "serious risk": "Serious regulatory risk identified.",
    "death": "Critical patient safety issue detected.",
    "life-threatening": "Life-threatening event detected.",
    "hospitalization": "Hospitalization reported.",
    "toxicity": "Potential toxicity concern."
}


def detect_risk(text):

    text_lower = text.lower()

    detected_keywords = []
    reasons = []

    for keyword, reason in HIGH_RISK_KEYWORDS.items():

        if keyword in text_lower:
            detected_keywords.append(keyword)
            reasons.append(reason)

    if detected_keywords:

        return {
            "level": "HIGH",
            "keywords": detected_keywords,
            "reasons": reasons
        }

    return {
        "level": "NORMAL",
        "keywords": [],
        "reasons": ["No major regulatory risk detected."]
    }