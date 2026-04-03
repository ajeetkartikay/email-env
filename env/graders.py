def grade_response(email: str, response: str, task_id: str = "task_1") -> float:
    if not response or len(response.strip()) < 10:
        return 0.0

    response_lower = response.lower()
    score = 0.0

    # ── 1. APOLOGY CHECK (0.15) ─────────────────────────────────────
    apology_words = ["sorry", "apologize", "apologies", "regret", "sincerely apologize"]
    if any(word in response_lower for word in apology_words):
        score += 0.15

    # ── 2. SOLUTION CHECK (0.15) ─────────────────────────────────────
    solution_words = ["resolve", "fix", "refund", "replace", "escalate",
                      "help", "assist", "process", "arrange", "dispatch",
                      "investigate", "correct", "address"]
    if any(word in response_lower for word in solution_words):
        score += 0.15

    # ── 3. POLITENESS CHECK (0.10) ───────────────────────────────────
    polite_words = ["thank", "appreciate", "understand", "valued",
                    "important", "priority", "pleased", "happy to help"]
    if any(word in response_lower for word in polite_words):
        score += 0.10

    # ── 4. ISSUE ACKNOWLEDGEMENT (0.10) ──────────────────────────────
    issue_words = ["delay", "delivery", "order", "issue", "problem",
                   "complaint", "refund", "billing", "wrong item",
                   "inconvenience", "concern", "error"]
    matches = sum(1 for word in issue_words if word in response_lower)
    score += min(matches * 0.05, 0.10)

    # ── 5. LENGTH SCORING (0.10) ──────────────────────────────────────
    word_count = len(response.split())
    if word_count < 20:
        score += 0.0       # too short
    elif word_count < 50:
        score += 0.05      # acceptable
    elif word_count <= 200:
        score += 0.10      # ideal length
    else:
        score += 0.05      # too long, penalize slightly

    # ── 6. STRUCTURE SCORING (0.15) ───────────────────────────────────
    structure_score = 0.0
    # has greeting
    greetings = ["dear", "hello", "hi ", "good morning", "good afternoon"]
    if any(g in response_lower for g in greetings):
        structure_score += 0.05
    # has closing
    closings = ["sincerely", "regards", "best wishes", "thank you",
                "warm regards", "yours truly"]
    if any(c in response_lower for c in closings):
        structure_score += 0.05
    # has proper punctuation/paragraphs
    if "\n" in response or len(response) > 100:
        structure_score += 0.05
    score += structure_score

    # ── 7. TONE CHECK (0.15) ──────────────────────────────────────────
    # penalize rude tone
    rude_words = ["not my problem", "not our fault", "you should have",
                  "impossible", "never", "can't help", "cannot help",
                  "not possible", "ridiculous", "your fault"]
    if any(word in response_lower for word in rude_words):
        score -= 0.20      # heavy penalty for rude tone

    # professional tone bonus
    professional_words = ["please", "certainly", "absolutely", "immediately",
                         "priority", "dedicated", "committed", "ensure"]
    prof_matches = sum(1 for word in professional_words if word in response_lower)
    score += min(prof_matches * 0.03, 0.10)

    # ── 8. TASK-SPECIFIC SCORING ──────────────────────────────────────
    if task_id == "task_1":
        # Easy: refund request — check for refund confirmation
        if any(w in response_lower for w in ["refund", "return", "reimburse"]):
            score += 0.05

    elif task_id == "task_2":
        # Medium: angry customer — check for de-escalation
        if any(w in response_lower for w in ["understand your frustration",
                                              "completely understand",
                                              "deeply sorry",
                                              "sincerely apologize"]):
            score += 0.05

    elif task_id == "task_3":
        # Hard: multi-issue — check if ALL issues addressed
        issues_addressed = 0
        if any(w in response_lower for w in ["wrong item", "incorrect item", "item"]):
            issues_addressed += 1
        if any(w in response_lower for w in ["billing", "charge", "payment"]):
            issues_addressed += 1
        if any(w in response_lower for w in ["support", "response", "team"]):
            issues_addressed += 1
        score += issues_addressed * 0.05  # up to 0.15 bonus

    # ── 9. CUSTOMER SATISFACTION TRACKING ────────────────────────────
    satisfaction_signals = ["happy to help", "here for you", "reach out anytime",
                            "at your service", "always here", "feel free to contact"]
    if any(s in response_lower for s in satisfaction_signals):
        score += 0.05

    return round(min(max(score, 0.0), 1.0), 2)