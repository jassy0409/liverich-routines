---
name: lrm-escalation-watchdog
description: Hourly scan of active fan threads across LRM accounts for serious complaints, anger, or account-risk signals. On a hit, post an alert to the MODEL's team channel tagging the on-shift chatter and @Jassy for a quick response. Read-only against OnlyFans; only writes are internal Slack alerts. Use when a manager says 'run the escalation watchdog', 'check for angry fans', or as the scheduled hourly routine.
---

# LRM Escalation Watchdog

Catch serious fan complaints early. Each run scans recent fan activity across the
LRM accounts, flags threads where a fan is angry / feels overcharged / is threatening
the account, then posts an alert to the model's team channel tagging the on-shift
chatter and @Jassy so a human handles it fast. The chatter's job is to STOP and
escalate, never to decide.

Read-only against OnlyFans. The only writes are internal Slack alerts. Never messages
the fan. Never quotes explicit content (see the scorecard skill's explicit-content rule).

## The self-contained routine prompt

This is the prompt the schedule runs. It does not depend on this file at run time.

> Run the LRM escalation watchdog for BOTH Shantal and Karina. This prompt is self contained. Work through the OnlyFans MCP connector (read only, never send anything to a fan) and Slack (post AS Jassy, the authorizing user, never a bot persona). Do both models in order, Shantal first then Karina. If one model's scan fails, still complete the other and note what failed at the end; never post a guessed alert.
>
> SCAN WINDOW (critical): scan fan messages from the last 90 minutes, using UTC timestamps from the API. Read ONLY the fan's INCOMING messages (isSentByMe false) and exclude every message with isFromQueue true (those are scheduled auto sends, not real fan activity). Process large tool payloads out of context (subagent or slice script), never pull a full thread into the main context.
>
> ACCOUNTS
> Shantal: acct_508c667e12d24250b75ae3d990594010. Karina paid: acct_48be256caa4c484cbab6774a098c4edb. Karina free: acct_bd0c6dda969f4631b02b3a9524fa44be (worked by the Karina roster, alert it as Karina).
>
> DETECTION METHOD, per account: listChats with filter unread (limit 20, skip_users all) plus listChats order recent (limit 15, skip_users all) to find threads with fan activity in the window. For each active thread listChatMessages (limit 20, order desc, skip_users all) and read the fan's recent incoming messages only.
>
> ESCALATION SIGNALS in the fan's words:
> CRITICAL: scam, report you, refund, chargeback, dispute, my bank, block you, turning off renew, unsubscribing over this.
> HIGH: overcharged, too expensive, why did you charge, others paid less, my friend got it for, everyone else gets, double charged, you took it back or clawed it back or pulled it back after paying, not fair, transactional, you scammed me, tipped and got nothing.
> REVIEW: repeated angry messages, all caps venting, "I'm done", "disappointed", demanding a manager.
> A price question from a fan who is shopping is NOT a complaint. When genuinely unsure, flag it: a false alert is cheap, a missed chargeback is not.
>
> DEDUPE: before posting, check the target channel for an alert on the same fan within the last 6 hours (slack_read_channel). If one exists, skip silently.
>
> ON SHIFT CHATTER, by current PHT time (PHT = UTC+8):
> Shantal: graveyard 11pm to 7am = Aaliyah <@U09U798V24X>, morning 7am to 3pm = Trisha <@U08H7941KTN>, afternoon 3pm to 11pm = Arsel <@U0B06PSRL83>.
> Karina: graveyard = Leigh <@U0AHFGZ5ZM2>, morning = MJ <@U06ALHQ6PUH>, afternoon = Alyzha <@U0B38R4A37S>.
> Days off (tag Jeffrey <@U06AJLM4JM7> instead): Trisha and MJ Sunday, Arsel and Alyzha Monday, Aaliyah and Leigh Tuesday nights.
>
> ALERT ACTION, one Slack message per tripped thread, posted to the MODEL's team channel:
> Shantal hits go to #shantal-team (channel_id C09P2UMSE2G). Karina hits (paid or free page) go to #karina-team-reports (channel_id C0B38BXSM88, private).
> Message format, keep exactly this shape:
> :rotating_light: ESCALATION ALERT, <Model>, fan <first name or display name>
> <@onShiftChatterID> <@U069Z6RFJR4>
> Severity: CRITICAL or HIGH or REVIEW
> What tripped it: one short non explicit sentence, for example "fan says he was overcharged versus a friend and wants a refund"
> Thread: fan username
> STOP. Do not reply with an offer, a discount, or more sales. Do not make a decision. Hold the thread until Jassy gives direction.
>
> STYLE RULES: fan first name or display name only, never quote explicit message text, no dash symbols anywhere in visible text (rewrite to avoid them), no @channel, plain direct wording. If nothing trips on either model, post nothing and end quietly. At the end report which threads tripped, which channels were alerted, and any account whose scan failed.

## Cadence

Hourly. Cron trigger (off the :00 mark on purpose):

```
13 * * * *
```

Each run scans the last ~90 minutes so nothing falls in the gap between runs.
A clean run posts nothing.

## Safety

Read-only against OnlyFans. Never sends anything to a fan. Only writes are Slack
alerts to the two internal team channels. Never reproduces explicit content. When a
thread's severity is genuinely ambiguous, err toward alerting so a human can judge.
