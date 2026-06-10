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


# --- Tests targeting the bug we fixed: a non-number guess used to burn an attempt. ---
# app.py only increments st.session_state.attempts when parse_guess reports ok=True, so the
# fix is correct as long as parse_guess flags bad input as not-ok and good input as ok. These
# tests pin that contract (the part of the rule that can be tested without Streamlit).

def test_non_number_guess_is_not_ok():
    # "abc" is not a number -> ok is False, so app.py must NOT count an attempt.
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_empty_guess_is_not_ok():
    # Empty input -> ok is False, so no attempt is spent.
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_valid_guess_is_ok():
    # A real number -> ok is True, which is the only case that spends an attempt.
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None
