def classify_issue(message: str):
    message = message.lower()

    if "error" in message or "not working" in message:
        return "TIER_2", "MEDIUM"

    if "crash" in message or "data loss" in message:
        return "TIER_3", "HIGH"

    return "TIER_1", "LOW"
