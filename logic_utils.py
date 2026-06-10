# FIX: Refactored core game logic out of app.py into logic_utils.py using the AI
# assistant in agent mode, so the logic is testable without Streamlit and the UI stays
# thin. Bug fixes are kept here at the source.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: hint messages were swapped — a guess ABOVE the secret is "Too High" and must
    # tell the player to go LOWER (the starter had it backwards). Verified by test +
    # live play. Dead str-vs-int compare branch removed; secret is always an int.
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: win formula used (attempt_number + 1) which double-counted (attempts is already
    # incremented before this call), so a perfect first-guess game didn't score max. Now
    # (attempt_number - 1). Both wrong outcomes apply a symmetric -5 (removed the bogus
    # even-attempt +5 reward that paid out for a wrong "Too High" guess).
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
