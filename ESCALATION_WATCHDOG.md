---
name: lrm-escalation-watchdog
description: Hourly scan of active fan threads across LRM accounts for serious complaints, anger, or account-risk signals. On a hit, post an alert into the on-shift chatter's management channel telling them to stop and escalate, and tag @Jassy for a quick response. Read-only against OnlyFans; only writes are internal Slack alerts. Use when a manager says 'run the escalation watchdog', 'check for angry fans', or as the scheduled per-hour routine.
---

# LRM Escalation Watchdog

Catch serious fan complaints early. Each run scans recent fan activity across the
LRM accounts, flags threads where a fan is angry / feels overcharged / is threatening
the account, then alerts the chatter working that shift and tags @Jassy so a human
handles it fast. The chatter's job is to STOP and escalate, never to decide.

Read-only against OnlyFans. The only writes are internal Slack alerts. Never messages
the fan. Never quotes explicit content (see the scorecard skill's explicit-content rule).

## Accounts

- Shantal: `acct_508c667e12d24250b75ae3d990594010` (uid 4669068)
- Karina VIP: `acct_48be256caa4c484cbab6774a098c4edb` (uid 221746288)
- Karina Free: `acct_bd0c6dda969f4631b02b3a9524fa44be` (uid 364264020)

## Shift -> chatter -> channel (PHT = UTC+8)

Same roster as the chatter-scorecard skill. Pick the on-shift chatter by the CURRENT PHT time.

| Account | Shift (PHT) | UTC window | Chatter | Mgmt channel | Chatter Slack ID |
|---|---|---|---|---|---|
| Shantal | graveyard 11pm-7am | 15:00-23:00 | Aaliyah | #aaliyah-management C09U784EE23 | U09U798V24X |
| Shantal | morning 7am-3pm | 23:00 prev-07:00 | Trisha | #trisha-management C08FFLCF92N | U08H7941KTN |
| Shantal | afternoon 3pm-11pm | 07:00-15:00 | Arsel | #john-arsel-management C0B0D5MH742 | U0B06PSRL83 |
| Karina | graveyard 11pm-7am | 15:00-23:00 | Leigh | #leigh-management C0AHBUAPXJN | U0AHFGZ5ZM2 |
| Karina | morning 7am-3pm | 23:00 prev-07:00 | MJ | #mj-management C07435SAD42 | U06ALHQ6PUH |
| Karina | afternoon 3pm-11pm | 07:00-15:00 | Alyzha | #alyzha-management C0B2EGZ5DDG | U0B38R4A37S |

Jeffrey (`U06AJLM4JM7`) covers off-days (Trisha/MJ Sun, Arsel/Alyzha Mon, Aaliyah/Leigh Tue nights).
If the covering chatter is on, tag them instead and post to their channel.
Karina Free is worked by the Karina roster; attribute it to the Karina on-shift chatter.

**Escalation contact:** always also tag @Jassy `U069Z6RFJR4` on every alert.

## Escalation signals (read the FAN's INCOMING messages only)

Scan messages the fan sent in the last ~90 minutes (`isSentByMe:false`; exclude
`isFromQueue:true`). Trip on any of:

- **Account-risk / legal (CRITICAL):** scam, report you, refund, chargeback, dispute, my bank, block you, "turning off renew", unsubscribing because of this.
- **Overcharge / pricing (HIGH):** overcharged, too expensive, "why did you charge", "others paid less", "my friend got it for", "everyone else gets", double charged.
- **Trust / feeling cheated (HIGH):** "you took it back", "clawed it back", "pulled it back after I paid", "not fair", "transactional", "you scammed me", "I tipped and got nothing".
- **General anger (REVIEW):** repeated angry messages, all-caps venting, "I'm done", "disappointed", demanding a manager.

Judgement call, made by reading the thread each run. When unsure, flag it — a false alert is cheap, a missed chargeback is not.

## Detection method

1. For each account, `listChats` (newest first) to find threads active in the scan window; prioritise `unreadMessagesCount>0` and `hasUnreadTips`.
2. For each active thread, `listChatMessages(account, chat_id, limit=20, order='desc', skip_users='all')`.
3. Read only the fan's incoming messages in the last ~90 min. Exclude `isFromQueue:true`.
4. Assign severity CRITICAL / HIGH / REVIEW from the signals above.
5. Large tool payloads auto-save to disk — process them out of context (a subagent or a slice script), never pull a full thread into the main context.
6. **Dedupe:** do not re-alert a thread already alerted in the last 6 hours. Track by the fan's `chat_id` + the id of the message that tripped it (keep a short note in `watchdog_state.json` in this folder, or check the channel for an existing alert on that fan today).

## Alert action (per tripped thread)

Post ONE message to the on-shift chatter's management channel:

```
:rotating_light: ESCALATION — <Account> — <fan first name / display name>
<@chatterID> <@U069Z6RFJR4>
Severity: <CRITICAL|HIGH|REVIEW>
What tripped it: <one non-explicit line, e.g. "fan says he was overcharged vs a friend and wants a refund">
Thread: <fan username / link>

STOP. Do not reply with an offer, a discount, or more sales. Do not make a decision.
Alerting @Jassy now — hold the thread until you get direction.
```

Rules for the alert copy: fan FIRST NAME or display name only, never the message text if it is explicit. No dashes inside sentences per LRM Slack style. Keep it to the block above.

## Cadence

Runs hourly via scheduled trigger. Each run scans the last ~90 minutes so nothing
falls in the gap between runs. If a run finds nothing, it posts nothing (silent).

Routine prompt (kept short — points here, does not restate the method):
> Run the LRM escalation watchdog. Follow the lrm-escalation-watchdog skill: scan the last ~90 minutes of fan activity on all three LRM accounts for the escalation signals, dedupe against the last 6 hours, and for each tripped thread post the alert block to the on-shift chatter's management channel tagging the chatter and @Jassy (U069Z6RFJR4). Read-only against OnlyFans, internal Slack alerts only, never quote explicit content. If nothing trips, do nothing.

## Safety

Read-only against OnlyFans. Never sends anything to a fan. Only writes are Slack
alerts to internal management channels. Never reproduces explicit content. When a
thread's severity is genuinely ambiguous, err toward alerting so a human can judge.
