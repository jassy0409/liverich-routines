# Shantal — Engagement Masses & Wall Posts Playbook

Per-shift free engagement cadence for Shantal Monique
(`acct_508c667e12d24250b75ae3d990594010`), matching the team's live pattern:
**1 opener → 1 reminder → 2 short bumps per shift**, plus wall posts.

## Targeting (matches house pattern)

- Audience: built-in `fans` list (~290k), free messages (no price).
- Always exclude lists: `1206433451`, `104020308`, `1248575538`.
- OnlyFans constraints learned the hard way:
  - `scheduledDate` format `Y-m-dTH:i:s.vZ` (e.g. `2026-07-16T07:30:00.000Z`), UTC.
  - Scheduling is only accepted for **dates after today** (no same-day). Same-day
    coverage must be sent live.
  - Rate limit: **one mass send per 10 seconds** — send sequentially, never batch.

## Shift windows (PHT = UTC+8; fan copy framed to US Pacific time of day)

| Shift (PHT) | UTC window | Fan-facing time of day |
|---|---|---|
| Afternoon 3pm–11pm | 07:00–15:00 | US late night → early morning |
| Graveyard 11pm–7am | 15:00–23:00 | US morning → afternoon |
| Morning 7am–3pm | 23:00–07:00 | US evening → midnight |

## Send schedule + copy (per full day)

### Afternoon shift
| UTC | Type | Copy |
|---|---|---|
| 07:30 | Opener | It is late and you are the last thing on my mind before I try to sleep. Tell me you are still up with me tonight 🤍 |
| 09:30 | Reminder | Did you get a chance to open what I sent above? I saved it for the ones still awake with me 😏 |
| 11:30 | Bump | Still right above for you. Do not let this one slip by 😌 |
| 14:00 | Bump | Good morning. Before you start your day, this is your last chance to see what is waiting above 🤍 |

### Graveyard shift
| UTC | Type | Copy |
|---|---|---|
| 15:30 | Opener | Good morning. You are the first person I wanted to talk to today. Tell me one thing you are looking forward to 🤍 |
| 17:30 | Reminder | Did you get a chance to look at what I left for you above? I really did have you in mind when I made it 😏 |
| 19:30 | Bump | It is still right above waiting for you. Do not let your afternoon get away without it 😌 |
| 22:00 | Bump | Last call on the one above before I move on to something new 🤍 |

### Morning shift
| UTC | Type | Copy |
|---|---|---|
| 23:30 | Opener | How was your day? I have been thinking about you and I am ready to unwind together tonight. Tell me all about it 🥰 |
| +1d 01:30 | Reminder | Have you opened the one I sent above yet? It is exactly the kind of thing to enjoy once your evening slows down 😏 |
| +1d 03:30 | Bump | Still sitting above for you. This is the perfect time to treat yourself 😌 |
| +1d 06:00 | Bump | Last chance before the night ends. What is above will not be there much longer 🤍 |

Reminders/bumps are generic — they point at whatever PPV is sitting "above" in
the chat, so they compose with whatever the shift chatter is selling.

## Wall posts (insta-style, text-only, Shantal voice)

Voice rules: personal and warm, proper sentences, no "hey", no pet names, ends
with a question to drive comments.

Weekend examples:
- Slow Sunday, coffee in hand, and absolutely nowhere to be 🤍 These lazy weekend days are my favorite. Tell me how you are spending yours.
- Sunday reset: soft light, my favorite playlist, and that easy weekend glow 😌 What is putting you in a good mood today?

Weekday examples:
- Coffee in hand and taking a slow moment before the day gets busy 🤍 Midweek always feels like the perfect time for a little reset. Tell me how your Wednesday is going.
- Soft light, my favorite playlist, and that easy glow to carry me through the week 😌 What is one thing making you smile today?

## Coordination notes

- The chatter team also sends masses live and unsends older ones as cleanup.
  Before scheduling a day, check `massMessages` for that date to avoid
  double-covering a day the team already ran.
- Jeffrey covers Princess's shift (Shantal afternoon 3–11pm PHT) every Monday PHT.
