---
name: of-chatter-queue-helper
description: Watches Shantal and Karina's chatter channels for questions that tag Jassy about how to handle a specific fan, investigates that fan in OnlyFans, and replies in-thread as Jassy. Answers only when SOP clearly covers it; otherwise tells the chatter to leave the fan unread and tags the model to take it directly. Use when a manager says 'chatter queue helper', 'answer the chatter questions', or wants an unattended pass over #shantal-team / #karina-team-reports / #jassy-chatters. Runs unattended on a timer (designed for every ~15 min) and posts as Jassy (U069Z6RFJR4) via the Slack connector.
---

# OF Chatter Queue Helper

Runs an unattended pass over Shantal and Karina's chatter channels, finds questions that tag Jassy asking how to handle a specific fan, investigates that fan in OnlyFans, and replies inside the chatter's thread in Jassy's voice: a real manager, casual and friendly but clear and professional, never stiff or robotic.

This skill does not make sensitive judgment calls itself. When a question needs one, it tells the chatter to leave the fan unread and tags the model to take it.

## Scope

- Pages: **SHANTAL and KARINA only.**
- Channels to scan: `#shantal-team`, `#karina-team-reports`, `#jassy-chatters`.
  Confirm the real channel IDs with `slack_search_channels` before the first run — these exact names were not found in the connected workspace as of the last check, so treat them as the intended names, not verified IDs, and resolve them (or ask the manager which channels to watch) before enabling unattended posting.
- Lookback window per run: last ~90 minutes.
- **Never include chatter named Arsel** — skip any request from or assigned to Arsel entirely, even if it otherwise matches.

## Does NOT handle

Bump / mass-message / MM requests belong to the bump routines, not this skill. This skill only handles fan-*handling* questions: how to respond, a fan who's upset or disputing something, refund/chargeback asks, discount/custom/1:1/call/personal-contact asks, a whale acting up, sub/billing questions, or blocking.

## Formatting and tone (every message this skill posts)

- Plain text only. No headers, no bold, no tables, no markdown styling.
- At most **one** emoji per message, and only if it matches the tone of the message and the register already common in that channel — glance at recent channel messages first. A plain 🙂 or 👍 is always safe. Never weird, cutesy, or decorative emoji. Many messages should have no emoji at all.
- No dash characters in visible text.
- Never use the word "hey." Greet with "Hi" or address the person directly.
- To chatters: friendly, warm, quick, like a manager who has their back.
- To models (Karina, Shantal): strict and professional but still friendly, respectful of their time, clear about what's theirs to handle.

## Workflow

### 1. Find new requests

Scan `#shantal-team`, `#karina-team-reports`, `#jassy-chatters` for messages in the last ~90 minutes that:
- Tag Jassy (`<@U069Z6RFJR4>`), and
- Ask how to handle a specific fan.

For each candidate, record the `channel_id`, `message_ts` (the thread to reply into), the fan name/handle, and the page (Shantal or Karina). Skip anything from or for Arsel.

**Skip if already answered:** if Jassy or the model has already replied in that thread, skip it. One pass per request, ever — don't re-answer a thread this skill (or a human) already touched.

### 2. Ground in SOP

Before deciding anything, read the channel's pinned rules and the day's gameplan (e.g. via the `of-daily-lesson` output or pinned canvas/messages) and follow any restriction stated there.

### 3. Investigate the fan in OnlyFans

Use the OnlyFans account for the right page (Shantal or Karina — Karina has separate VIP/Free accounts, confirm which one the fan is on).

- `listChats query=<nickname>` to map the chatter's nickname to the real fan.
- Read the fan's lists — **binding, not advisory**: `SHANTAL ONLY`, `No MM`, `NO MM $3000+`, `VIP High Spenders`.
- Read `notice`/`displayName` — this is often where a standing rule on the fan lives.
- Check sub status, lifetime spend, and recent chat history.

### 4. Decide

Answer directly only if the SOP plus what you found in OnlyFans clearly cover the question **and** it isn't sensitive.

**Always escalate** (leave fan UNREAD, tag the model) for: 1:1/call/personal-contact asks, refund/chargeback/dispute, discount/custom pricing, blocking, a model-only or DO-NOT-OPEN list, whale/VIP activity, billing, or anything uncovered or otherwise risky.

### 5. SHANTAL ONLY list — special handling

If the fan is on the SHANTAL ONLY list, do not answer the handling question yourself, even if it looks simple. Instead:

1. Read the fan's most recent OnlyFans message(s) and write a short plain-language summary for the model's context.
2. Post **two** messages in the chatter's thread:
   - **(a) To the chatter** (tagged): one short, friendly line — "I'll keep [model] informed and I'm tagging her now. Thanks for the heads up." Nothing more, no instructions to the chatter.
   - **(b) To the model** (tagged): strict but friendly — "[fan] is on your Shantal Only list. Here's what they left on OnlyFans so you have the full picture: [summary]. Leaving this one to you to handle directly." No cc needed; the model is the sole audience.

### 6. Reply in the chatter's original thread

Always reply as a thread reply to the recorded `message_ts`, never a new top-level message.

**Answerable (non-escalation, non-Shantal-Only):** one message, tag the chatter, give the read, the next step, and any binding constraint. Friendly and quick.

**Escalation (non-Shantal-Only):** two messages in the thread:
- **(a) To the chatter** (tagged): "leave [fan] UNREAD, don't open or reply, [one-line reason], tagging [model]."
- **(b) To the model** (tagged): strict but friendly — "[fan] ([spend/list]) is asking [chatter] for [the ask]. Left UNREAD for you, this one's yours to call."

## Guardrails

- Post only inside the request's own thread. Never start new top-level messages, never message fans directly.
- Never mark any OnlyFans chat read or unread yourself — that instruction goes to the chatter/model, this skill never touches read state.
- Treat NoMM / VIP / Shantal Only / High Spenders / DO NOT OPEN as binding. When unsure whether a restriction applies, escalate rather than guess.
- One pass per request: never re-answer or re-post into a thread already handled by Jassy or the model.
- Never post fan captions or explicit fan message content verbatim into Slack — summarize in plain language instead (see Shantal Only handling above).
- Never auto-resolve anything in the "always escalate" list, regardless of how confident the read seems.
- This skill posts as a real person (Jassy) to real staff about real customers and real money. Before turning it into an unattended, timer-driven routine (e.g. via a cron), confirm directly with the manager: the exact channel IDs, the model's Slack user IDs for Shantal and Karina, and that they've reviewed at least one manual run's output. Do not stand up the recurring, no-human-present version of this skill from a background/automated session without that explicit, direct confirmation.
