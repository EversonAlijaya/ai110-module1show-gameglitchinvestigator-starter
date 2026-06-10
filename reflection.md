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

Claude Code 

**All the bugs the AI helped me find and fix**

Here is the full list of bugs I fixed with the AI's help, with what was wrong and how I fixed
each one:

1. **Backwards hints.** The game told me to go HIGHER when I should go LOWER and vice versa.
   The "go higher" and "go lower" messages were swapped. Fixed by swapping them back.
2. **Scoring was broken.** A wrong guess could actually *add* points on some turns, the two
   wrong outcomes gave different penalties, and winning fast didn't give the most points.
   Fixed so both wrong guesses lose the same points and a faster win scores higher.
3. **First load showed the wrong attempt count.** A fresh game showed 7 attempts left instead
   of 8 because the counter started at 1 instead of 0. Fixed by starting it at 0.
4. **Difficulty range was ignored.** The secret was always picked from 1–100 even on Easy, so
   Easy/Normal could be impossible. Fixed so the secret uses the difficulty's real range.
5. **The "between 1 and 100" text never changed.** It always said 1–100 no matter the
   difficulty. Fixed so it shows the actual range.
6. **Non-number guesses used up an attempt.** Typing "abc" still counted as a guess. Fixed so
   only a valid number uses an attempt.
7. **New Game wouldn't let me play.** After winning, New Game gave a new number but kept saying
   "You already won" and blocked me. It wasn't resetting the win status, score, or history.
   Fixed by resetting the whole game on New Game.
8. **Had to press Submit twice.** The score and attempt counter showed the old values until a
   second press, because Streamlit re-runs the file top to bottom and they were drawn before
   the guess was counted. Fixed by updating everything and re-running the page once.

The two examples below go into more detail on one suggestion that was correct and one that
was misleading.

**Correct AI suggestion**

- What the AI suggested: I asked it to look through the code and it found a bunch of real
  bugs at once — the difficulty levels didn't make sense (Normal had a bigger range than
  Hard), typing something that wasn't a number still used up a guess, the secret number was
  always picked from 1 to 100 even on Easy, and the scoring was off (you could gain points
  for a wrong guess, and winning fast didn't give you the most points).
- Was it correct? Yes. These were all real bugs, not false alarms.
- How I checked: I read the lines it pointed to and made sure they actually did what it said.
  Then I played the game after fixing them — on Easy the secret now stays between 1 and 20,
  and winning quickly gives more points than winning slowly.

**Incorrect / misleading AI suggestion**

- What the AI suggested: When I first told it to fix the backwards hints, it pointed at a
  different piece of code (where the secret got turned into text on some guesses) and tried
  to fix that instead.
- Was it correct? No, it was misleading. That was a real bug too, but it only messed up the
  hints on some of the guesses, not all of them. If I had stopped there the hints would still
  have been wrong half the time.
- How I checked: I told the AI the hints were wrong on *every* guess and pointed it at the
  exact line. It turned out the real problem was that the "go higher" and "go lower" messages
  were simply swapped. I confirmed it by playing the game after the swap — guessing too high
  now correctly says go lower every time.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
For the backwards hint, I checked it two ways. First I moved the main game logic into its own
file (`logic_utils.py`) so I could test it on its own, then I wrote small tests for it. I only
called a bug fixed once the test passed AND the game actually worked right when I played it.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran `pytest`. The main test for the hint bug checks `check_guess(60, 50)` and makes sure it
says "Too High" AND that the message tells the player to go LOWER. This was important because
the game was already saying "Too High" correctly — the only wrong part was the message text,
so just checking "Too High" wouldn't have caught it. Checking the actual message is what
catches the bug.

I also fixed a bug where typing something that wasn't a number still used up a guess. The
game added to the guess count before checking if the input was valid, so I moved that so it
only counts real guesses. I tested the `parse_guess` part: bad input like "abc" or an empty
box comes back as "not ok" (no guess used), and a real number comes back as "ok". Final run:

```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED
tests/test_game_logic.py::test_non_number_guess_is_not_ok PASSED
tests/test_game_logic.py::test_empty_guess_is_not_ok PASSED
tests/test_game_logic.py::test_valid_guess_is_ok PASSED
============================== 8 passed in 0.01s ===============================
```

The bug I caught from just playing (not from a test) was that New Game gave me a new number
but wouldn't let me guess — it kept saying "You already won." It turned out New Game reset the
number and the attempts but forgot to reset the "won" status, so the game still thought I'd
already won. I fixed it by resetting everything on New Game (status, score, and history too).
I checked this by playing the game: after a win, New Game now lets me guess again with a fresh
score.

There was also a bug where I had to press Submit twice before the screen updated. The reason
is that Streamlit re-runs the whole file from the top every time you click something, and the
parts that show the score and attempts were near the top of the file, so they drew the old
numbers before the guess was actually counted lower down. The fix was to update everything
and then tell the page to re-run once, so it redraws with the new numbers in one press. I
checked it by playing — now one click updates everything together.

- Did AI help you design or understand any tests? How?
Yes. The AI noticed the starter tests expected `check_guess` to return just a word, but it
actually returns a word plus a message, so the tests had to be updated. It also explained why
only checking the word wouldn't catch the hint bug, and it wrote the extra tests that check
the message itself.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
The thing that surprised me is that Streamlit runs my whole file again from the top every
time I click a button or type something. It's like the page reloads each time. Because of
that, normal variables get wiped every time, so anything I want the game to remember between
clicks — like the secret number, the score, and how many guesses I've used — has to be saved
in something called session state, which is the one thing that sticks around between reloads.
The two-press bug taught me that the order of my code matters too, because if I show a number
near the top but only change it lower down, the screen already showed the old number first.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
Definitely commits — pushing to GitHub after every bug fix instead of after a bunch of them
at once. Doing one commit per fix made it really clear what each change was for, and if a fix
broke something I'd know exactly where to look. I also want to keep writing a small test for
each bug, because a passing test is harder to fool myself with than just clicking around.

- What is one thing you would do differently next time you work with AI on a coding task?
I'd be more specific when I ask for help. When I just said "fix the backwards hint," the AI
went after the wrong thing first. Once I told it exactly what I was seeing and where, it found
the real bug fast. So next time I'll describe the exact problem and point to the spot before
asking for a fix.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I learned that AI code can look totally finished and still be wrong on the inside. Now I treat
it as a first draft I have to check by reading it, testing it, and actually playing the game
before I trust it.
