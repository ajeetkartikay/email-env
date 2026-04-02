def grade_response(email: str, response: str) -> float:
    if not response or len(response.strip()) < 10:
        return 0.0

    response_lower = response.lower()
    email_lower = email.lower()
    score = 0.0

    # +0.3 for apologizing
    if any(word in response_lower for word in ["sorry", "apologize", "apologies"]):
        score += 0.3

    # +0.3 for offering a solution
    if any(word in response_lower for word in ["resolve", "fix", "refund", "replace", "escalate", "help", "assist"]):
        score += 0.3

    # +0.2 for being polite
    if any(word in response_lower for word in ["thank", "appreciate", "understand"]):
        score += 0.2

    # +0.2 for acknowledging the issue
    if any(word in response_lower for word in ["delay", "delivery", "order", "issue", "problem"]):
        score += 0.2

    return min(round(score, 2), 1.0)