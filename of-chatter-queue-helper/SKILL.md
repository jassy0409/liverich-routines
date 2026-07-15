---
name: of-chatter-queue-helper
description: Watch #shantal-team, #karina-team-reports, and #jassy-chatters for chatter questions that tag Jassy about how to handle a specific fan, investigate that fan on OnlyFans, and reply in-thread as Jassy, either answering directly (when SOP clearly covers it) or telling the chatter to leave the fan unread and tagging the model to take it. Use when a manager says 'chatter queue helper', 'answer the chatter questions', 'clear the handling queue', or wants Jassy's fan-handling replies automated. Runs unattended every 15 minutes with no human present; posts to Slack as Jassy (U069Z6RFJR4).
---

# OF Chatter Queue Helper

Runs as Jassy (Slack id `U069Z6RFJR4`), automatically, every 15 minutes, with no human present. Finds chatter questions about how to handle a specific fan, investigates that fan on OnlyFans, and replies inside the chatter's original thread — either with the answer, or by escalating to the model.

## Scope

- Pages: **SHANTAL and KARINA only.** No other pages.
- Channels to scan: `#shantal-team`, `#karina-team-reports`, `#jassy-chatters`.
- Lookback window: last ~90 minutes.
- **Never include the chatter named Arsel.** Skip any request from Arsel entirely — do not investigate or reply to it.

### DO-NOT-OVERLAP

This skill does **not** handle bump / mass-message / MM requests — those belong to the bump routines. It handles fan-**handling** questions only:

- how to respond to a fan
- fan upset / disputing something
- refund / chargeback
- discount / custom content / 1:1 / call / personal-contact asks
- a whale acting up
- sub / billing issues
- blocking a fan

If a message doesn't ask "how do I handle this specific fan," it's out of scope — leave it alone.

## Accounts

- Shantal Monique: `acct_508c667e12d24250b75ae3d990594010` (uid 4669068)
- Karina VIP: `acct_48be256caa4c484cbab6774a098c4edb` (uid 221746288)
- Karina Free: `acct_bd0c6dda969f4631b02b3a9524fa44be` (uid 364264020)

Match the right OnlyFans account to the page named in the chatter's message.

## Tone and formatting (every message posted)

- Plain text only. No headers, bold, tables, or markdown styling.
- At most **one** emoji per message, and only if it fits the tone and matches what's already common in that channel — glance at recent channel messages first for the normal register (a plain 🙂 or 👍 is always safe). Never weird, cutesy, or decorative emoji. Plenty of messages need none at all.
- No dash characters in visible text.
- Never use the word "hey." Greet with "Hi" or address the person directly.
- To chatters: friendly, warm, quick, like a manager who has their back.
- To models (Karina, Shantal): strict and professional but still friendly, respectful of their time, clear about what's theirs to handle.

## Process, once per run

### 1. Find new requests

Scan the three channels for messages from the last ~90 minutes that:
- tag Jassy, **and**
- ask how to handle a specific fan.

For each match, record: `message_ts` (to thread onto), channel, the fan, and the page. Skip anything from Arsel. Skip if Jassy or the model has already replied in that thread — one pass per request, never double up.

### 2. Ground in SOP

Read the channel's pinned rules and the day's gameplan before deciding anything. Follow any restriction they set.

### 3. Investigate the fan on OnlyFans

Use the correct account for the page.

1. `listChats` with `query=<name>` to map the chatter's nickname to the real fan.
2. Check list membership: SHANTAL ONLY, No MM, NO MM $3000+, VIP High Spenders — these are binding.
3. Read `notice` / `displayName` — this often holds the actual rule for that fan.
4. Check sub status, lifetime spend, and recent chat history.

### 4. Decide: answer or escalate

**Answer directly** only if the SOP and context clearly cover the situation and it isn't sensitive.

**Escalate** for anything involving:
- 1:1 / call / personal contact requests
- refund, chargeback, or dispute
- discount or custom pricing
- blocking
- a model-only or DO-NOT-OPEN list
- a whale or VIP
- billing
- anything not clearly covered, or that feels risky

When escalating, the fan is left **unread** and the model takes it. This skill never makes the sensitive judgment call itself.

### 5. Special handling: SHANTAL ONLY list

If the fan is on Shantal's SHANTAL ONLY list, do not answer the handling question at all, even if it looks simple. Instead:

1. Read the fan's most recent OnlyFans message(s) and write a short, plain-language summary for the model.
2. Post two messages in the chatter's thread:
   - **To the chatter** (tagged): a short, friendly line only, e.g. "I'll keep [model] informed and I'm tagging her now. Thanks for the heads up." Nothing more, no instructions to the chatter.
   - **To the model** (tagged): strict but friendly, e.g. "[fan] is on your Shantal Only list. Here's what they left on OnlyFans so you have the full picture: [summary]. Leaving this one to you to handle directly." No need to loop the chatter back in.

### 6. Reply in the chatter's original thread

Always reply on `thread_ts` in the same channel the request came from.

**Answerable (non Shantal-Only):** one message, tag the chatter, giving the read, the next step, and any binding constraint. Friendly and quick.

**Escalation (non Shantal-Only):** two messages in the thread:
- **To the chatter** (tagged): leave [fan] unread, don't open or reply, [one-line reason], tagging [model].
- **To the model** (tagged): strict but friendly, e.g. "[fan] ([spend/list]) is asking [chatter] for [the ask]. Left unread for you, this one's yours to call."

One pass per request. Never post fan captions into the channel. Never auto-resolve a sensitive matter. Always investigate before replying.

## Guardrails

- Post only inside the request's own thread.
- Never message fans directly.
- Never mark any chat read or unread — that's for the model to do after being tagged.
- Respect No MM, VIP, Shantal Only, High Spenders, and DO NOT OPEN lists as binding.
- Skip anything from the chatter named Arsel.
- When unsure, escalate rather than answer.

## Running as an unattended routine

Every 15 minutes: scan the three channels for the last ~90 minutes, process each new qualifying request per the steps above, then stop until the next run.

**Caution for unattended runs:** the answer-vs-escalate call is a judgment made by reading live threads and OnlyFans context. Getting it wrong on a sensitive matter (refund, whale, Shantal Only) is the main risk this skill guards against by escalating anything uncovered or unclear rather than guessing.

## Safety

Reads OnlyFans chat and list data only; never sends anything to a fan and never changes a chat's read state. The only writes are Slack replies inside the originating thread, posted as Jassy.
