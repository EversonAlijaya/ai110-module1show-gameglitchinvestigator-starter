from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# check_guess returns (outcome, message); these tests unpack the outcome.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New test targeting the bug we fixed: the high/low HINT MESSAGE was backwards. ---
# Outcome alone wasn't enough to catch it — the starter returned "Too High" but told the
# player to "Go HIGHER!". This pins the message direction.

def test_too_high_message_says_go_lower():
    # Guess 60 vs secret 50: guess is too high, so the hint must say go LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_too_low_message_says_go_higher():
    # Guess 40 vs secret 50: guess is too low, so the hint must say go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
