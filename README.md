# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game's purpose

A simple number-guessing game built with Streamlit. You pick a difficulty, the app picks a
secret number in that difficulty's range, and you guess until you get it or run out of
attempts. After each guess it tells you if you're too high or too low, tracks your score, and
lets you start a new game. The starter version was full of bugs that made it unfair or
impossible to win — the goal was to find and fix them.

### Bugs found

1. **Backwards hints** — it said "go higher" when you needed to go lower, and vice versa.
2. **Broken scoring** — a wrong guess could *add* points on some turns, the two wrong
   outcomes gave different penalties, and winning fast didn't give the most points.
3. **Wrong attempt count on first load** — a fresh game showed 7 attempts left instead of 8.
4. **Difficulty range ignored** — the secret was always picked from 1–100, even on Easy, so
   Easy/Normal could be impossible to win.
5. **Hardcoded range text** — the prompt always said "between 1 and 100" no matter the
   difficulty.
6. **Non-number guesses used an attempt** — typing "abc" still cost you a guess.
7. **New Game was broken** — after a win it gave a new number but kept saying "You already
   won" and wouldn't let you play.
8. **Had to press Submit twice** — the score and attempts counter showed old values until a
   second press.

### Fixes applied

| Bug | Fix |
|-----|-----|
| Backwards hints | Swapped the "go higher"/"go lower" messages back to match the outcome |
| Broken scoring | Both wrong guesses now lose 5 points; a faster win scores higher |
| Wrong first-load count | Start the attempt counter at 0 to match New Game |
| Difficulty range ignored | Pick the secret using the difficulty's real range |
| Hardcoded range text | Show the actual low–high range for the chosen difficulty |
| Non-number guesses | Only count an attempt when the input is a valid number |
| New Game broken | Reset the full game state (status, score, history) on New Game |
| Press Submit twice | Update state, then re-run the page once so everything refreshes together |

The core game logic was also moved out of `app.py` into `logic_utils.py` so it can be tested
on its own, and each fix is marked with a `# FIX:` comment in the code.

## 📸 Demo Walkthrough

A walkthrough of the fixed game:

1. Run `python -m streamlit run app.py` and the game opens in the browser.
2. Pick a difficulty in the sidebar (Easy, Normal, or Hard). The range and number of attempts
   update to match, and the "Guess a number between X and Y" text shows the correct range.
3. Type a guess and click **Submit Guess 🚀**. In one press, the hint, the score, the
   "Attempts left" counter, and the Developer Debug Info all update together.
4. The hint is now correct — if your guess is too high it tells you to go LOWER, and if it's
   too low it tells you to go HIGHER.
5. Keep guessing. A correct guess shows balloons and a win message with your final score; if
   you run out of attempts the game tells you the secret and your score.
6. Click **New Game 🔁** to start over — it gives a fresh number in the right range and resets
   the score, attempts, and history so you can play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts ==============================
collected 8 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 12%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 25%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 37%]
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED     [ 50%]
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED     [ 62%]
tests/test_game_logic.py::test_non_number_guess_is_not_ok PASSED         [ 75%]
tests/test_game_logic.py::test_empty_guess_is_not_ok PASSED              [ 87%]
tests/test_game_logic.py::test_valid_guess_is_ok PASSED                  [100%]

============================== 8 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
