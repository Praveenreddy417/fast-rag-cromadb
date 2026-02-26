BLOCKED_WORDS = ["hack", "attack", "bypass"]

def check_guardrail(message: str):
    for word in BLOCKED_WORDS:
        if word in message.lower():
            return True, f"Blocked keyword detected: {word}"
    return False, None
