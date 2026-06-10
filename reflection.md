# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
the hints were backwards
new game did not work
the score did not make sense
the "attempts left" counter was behind by 1 guess
the first time i load the app it removes an attempt, where it shoud be 8 like when i press new game, it starts at 7



**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|guess was 67 |go higher hint | go lower hint| none|
|new game |restart the game but kept stats| did not restart the game| |
|used all number of attempts| showed corectly hopw many attempts i had left| when it said i had no attempts left and the game finished, it still said "attempts left : 1" | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Claude Code (Anthropic's CLI agent).

**Correct AI suggestion**

- What the AI suggested: When I asked it to scan `app.py`, it flagged several real bugs at
  once — the difficulty settings being inconsistent (Normal had a wider range than Hard),
  non-number guesses still burning an attempt, the secret number always being generated in
  the 1–100 range even on Easy/Normal (so those games could be unwinnable), and multiple
  scoring glitches (a wrong "Too High" guess *adding* +5 points on even attempts, "Too High"
  and "Too Low" giving different penalties, and the win formula using `attempt_number + 1`
  which double-penalized and meant a perfect first-guess game didn't award full points).
- Correct or misleading: Correct. Each of these was a genuine bug, not a false alarm.
- How I verified: I read the lines the AI pointed to and confirmed the logic myself — e.g.
  on the scoring, I traced that `attempts` is incremented at line 137 *before* `update_score`
  is called, so the `+ 1` really did double-count. After the fixes I played the game: New
  Game on Easy now produces secrets inside 1–20, and a fast win gives more points than a
  slow one. The `# FIX:` comments in `app.py` mark each confirmed change.

**Incorrect / misleading AI suggestion**

- What the AI suggested: When I first asked it to fix the backwards hints, it pointed at the
  code that casts the secret to a string on even attempts (`secret = str(...)`) and tried to
  remove that as the fix.
- Correct or misleading: Misleading — incomplete. That string cast *was* a real bug, but it
  only corrupted hints on even attempts; it did not explain why hints were wrong on **odd**
  attempts too. So accepting that fix alone would have left the game still giving wrong hints
  half the time.
- How I verified: I told the AI the hints were wrong on *every* guess, not just even ones,
  and pointed it at line 37. On re-checking, the real root cause was that the messages
  themselves were swapped — `guess > secret` ("Too High") returned "Go HIGHER!" instead of
  "Go LOWER!". I confirmed by playing the game after the message swap: guessing high now
  correctly says go lower on every attempt. The string-cast removal was still applied
  afterward as a separate, second fix.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
The biggest bug fix was the backwards hint. I decided it was fixed in two ways: first I
refactored the core logic (`check_guess`, `parse_guess`, `get_range_for_difficulty`,
`update_score`) out of `app.py` into `logic_utils.py` so it could be tested without
Streamlit, then I wrote pytest cases that pin the behavior. A bug only counted as fixed
once the matching test passed AND the live game behaved correctly when I played it.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran `pytest` from the repo root. The key test for the hint bug is
`test_too_high_message_says_go_lower`: it calls `check_guess(60, 50)` and asserts the
outcome is `"Too High"` AND that the message contains `"LOWER"`. This mattered because the
starter's outcome label was already "Too High" — the bug was only in the *message text*
("Go HIGHER!"), so a test that checked the outcome alone would have passed even with the
bug. Adding `"LOWER" in message` is what actually catches the regression. Final run:

```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED
============================== 5 passed in 0.01s ===============================
```

- Did AI help you design or understand any tests? How?
Yes. The AI pointed out that the three starter tests assumed `check_guess` returned a bare
string, while the real function returns a `(outcome, message)` tuple — so they had to be
updated to unpack the tuple, and it explained *why* an outcome-only assertion wouldn't have
caught the hint bug. It then generated the two message-direction tests that target exactly
the bug I fixed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
