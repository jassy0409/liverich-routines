# Instant Module Prompt — turn a directive into a lesson, exam, and team send

For managers running their own Chatter Playbook (set up per `TEAM-SETUP.md`).
Paste everything below into your Claude Code session (connected to your
playbook repo and your Slack), fill in the three blanks, and Claude builds and
sends the module end to end.

> **If you manage chatters on someone else's playbook:** don't run this
> yourself — send your directive to the playbook owner so there is one owner
> of the repo and the Slack channels.

---

```
INSTANT MODULE PROMPT — turn a directive into a lesson, exam, and team send

You are working in my Chatter Playbook repo (set up per TEAM-SETUP.md: module
pages + exams on GitHub Pages, exams auto-post scores and coaching to each
chatter's Slack management channel, roster.json is the source of truth).

═══ FILL IN ═══
1. THE DIRECTIVE (voice-memo transcript, leadership message, or my own
   observation of what the team is doing wrong):
   "<PASTE IT HERE>"
2. URGENCY: <"today — answer needed today, not tomorrow" OR "next weekly slot">
3. AUDIENCE: <"all chatters in roster.json" OR list specific names>
═══════════════

──────────────────────────────────────────────
THE LESSON — every module MUST contain these 7 parts, in this order
──────────────────────────────────────────────
1. A WORD FROM THE TOP — open with the directive's strongest lines quoted in
   a card, so chatters feel where this comes from and why it matters now.

2. THE MINDSET SHIFT — 3-4 numbered beliefs that reframe how the chatter
   should THINK about the situation before any technique. (Example:
   "a no is a direction, not a wall"; "the silent death is the real
   failure.") Each belief is one bold claim + 1-2 sentences of why.

3. THE CORE METHOD — one named, memorable framework the chatter can hold in
   their head on shift: a numbered pipeline, a ladder, a checklist, or a
   3-light system. Give it a name ("The Pipeline Rule", "The Ladder",
   "The Thermostat"). Maximum 5 steps. Each step gets a bold name + one
   line of how to use it.

4. THE PSYCHOLOGY — why the method works on the fan's side: desire,
   scarcity, curiosity, feeling seen, status. 3-4 short points. This is what
   separates a chatter who follows rules from one who understands the game.

5. MOCK CHATS — minimum 3 full worked threads in chat bubbles, each with a
   context line on top and a "why it works" line underneath:
   - at least one COMPLETE thread showing the method start-to-finish
     (including the fan's resistance and the close),
   - at least one bad-vs-good contrast,
   - at least one "what this is NOT" example showing the failure mode the
     directive complains about (and why it loses fans/money).
   All chat lines written in the models' actual voices, believable, specific,
   never generic. House rules apply inside every example: on-platform only,
   persistence through NEW angles and confidence — never guilt, begging,
   or spam.

6. GOLDEN RULES — 5-6 one-line rules that compress the whole module. A
   chatter should be able to screenshot this card alone and play correctly.

7. CTA — button to the module's exam.

──────────────────────────────────────────────
THE EXAM — must test the lesson, not trivia
──────────────────────────────────────────────
15 questions in the house 4-part shape, each mapped to a lesson part:
- Part 1 (5 multiple choice): Q1 tests the mindset shift, Q2 tests the core
  method, Q3 tests the psychology, Q4 tests the failure mode, Q5 tests the
  line between right and wrong execution. Wrong options must be plausible
  (the mistakes chatters actually make), not jokes.
- Part 2 (4 spot-the-mistake): real-looking bad chatter replies pulled from
  the failure modes in the directive.
- Part 3 (4 write-your-reply): live scenarios where the chatter must produce
  the method in their own model's voice.
- Part 4 (2 reflection): one "why does this matter" in their own words, one
  "what will you change on your next shift."
For every MC question also write: CORRECT (the letter), EXPLAIN (why, 1-2
sentences), and BEST (the exact line or flow to use — this feeds the
automatic Slack coaching and the performance review page).

──────────────────────────────────────────────
BUILD, VERIFY, SEND
──────────────────────────────────────────────
A. BUILD in the house format by copying the newest module's files:
   chatter edition (module-N-<slug>-chatter.html, playbook.css, dark pinned,
   phasebar), exam (copy newest module-N-exam-chatter.html; replace title,
   pill, hero, study-first link, questions, CORRECT/EXPLAIN/BEST, MODNUM,
   MODURL; keep the CONFIG roster and webhooks exactly as-is), manager guide
   (trainer script + coach notes + answer key + written rubric), review.html
   DATA entry, roster.json modules append, index.html + managers.html links.
B. VERIFY: node --check on the exam's final script block, commit, push, and
   confirm the GitHub Pages deploy is green BEFORE sending any link.
C. SEND one Slack message per chatter to their management channel from
   roster.json, tagged <@slackId>. Tone: warm but direct, open "Hi [name]"
   (never "Hey"), emojis at line ends only, no dashes, no word "tap".
   Include: the one-line why, the reading link, their personal exam link
   (?chatter=<key>), the urgency, one encouraging line. Internal management
   channels ONLY — never fans, never OnlyFans, never outside the roster.
D. REPORT: module name + links, who was messaged/skipped, and a per-model
   forwardable link pack (one block per model: reading link + each chatter's
   exam link).
```
