---
name: of-chatter-scorecard
description: Read a creator's recent direct messages and grade each chatter 0-100 on relationship-building, value-setting, VIP funnel, and avoiding dead-end replies, with real examples. Use when a manager says 'chatter scorecard', 'grade my chatters', or 'how are the chatters selling'. Deeper dig — reads full message history, slower. Can run unattended as a per-shift routine that renders an animated GIF card per chatter and posts a coaching report to that chatter's Slack management channel.
---

# OF Chatter Scorecard

Grade each chatter 0-100 across four pillars, render one animated LRM dark-style GIF card, and write a short coaching report in Jassy's tone focused on the weakest (red) pillar.

## Account scope

Run only on models the requesting manager owns. LRM accounts:
- Shantal Monique: `acct_508c667e12d24250b75ae3d990594010` (uid 4669068)
- Karina VIP: `acct_48be256caa4c484cbab6774a098c4edb` (uid 221746288)
- Karina Free: `acct_bd0c6dda969f4631b02b3a9524fa44be` (uid 364264020)

## Rosters and shift-to-UTC windows

PHT = UTC+8. Fan-facing copy is framed in PST time-of-day cues; scoring windows are in UTC.

| Account | Shift (PHT) | UTC window | Chatter | Slack mgmt channel | Chatter Slack ID |
|---|---|---|---|---|---|
| Shantal | graveyard 11pm-7am | 15:00-23:00 (same day) | Aaliyah | #aaliyah-management C09U784EE23 | U09U798V24X |
| Shantal | morning 7am-3pm | 23:00 prev - 07:00 | Trisha | #trisha-management C08FFLCF92N | U08H7941KTN |
| Shantal | afternoon 3pm-11pm | 07:00-15:00 | Princess | #princessf-management C0B5D3AJYB1 | U0B5Y66UDAQ |
| Karina | graveyard 11pm-7am | 15:00-23:00 (same day) | Leigh | #leigh-management C0AHBUAPXJN | U0AHFGZ5ZM2 |
| Karina | morning 7am-3pm | 23:00 prev - 07:00 | MJ | #mj-management C07435SAD42 | U06ALHQ6PUH |
| Karina | afternoon 3pm-11pm | 07:00-15:00 | Rosanna | #rosanna-management C0AUM8Z0SSD | U0AV2KV1DUG |

Jeffrey (U06AJLM4JM7) covers off-days. Days off: Trisha/MJ Sunday, Princess/Rosanna Monday (inherited from the afternoon slot — confirm with Jassy), Aaliyah/Leigh Tuesday nights. If a covering chatter worked the shift, attribute to whoever actually worked and post to the worker's channel. Roster updated Jul 17 2026: Arsel and Alyzha left the team; Princess took Shantal afternoons, Rosanna took Karina afternoons.

Attribution: the API has NO chatter-attribution field. Bin messages and sales by their PHT/UTC timestamp into the shift window. Card footer always reads "attribution by shift window" plus "threads read: [names]".

## Four-pillar rubric (each /25, overall /100)

1. **Relationship building** — warmth, personalization (uses fan's name), genuine two-way engagement, on-brand voice.
2. **Value setting** — landing PPV/tip sales, laddering after a yes, pricing to the fan, not leaving money on the table.
3. **VIP funnel** — working VIP-tagged fans, moving mid-spenders toward VIP/SVIP, protecting whales.
4. **Avoids dead ends** — answering real questions instead of deflecting, reading buyer signals, NOT over-pushing past a satisfied/done signal, NOT withholding after a purchase, NOT needy guilt-trip re-pokes.

Block + overall colour: >=80 green, 65-79 amber, <65 red. Pillar bar colour derives the same way from score*4. Weakest pillar is the report's focus.

## Restricted words (count from the CHATTER's OUTGOING messages only)

- **Shantal:** explicit anatomy terms, "dripping wet", "cheeky", "handsome", "hey", "baby", and pet names. Shantal voice is personal one-to-one, first names only, proper sentences, no "hey/hay", no pet names.
- **Karina:** lowercase bratty/playful voice. babe/baby/pet names are allowed ONLY for a VIP who is actively spending in that moment; count as a violation otherwise.

## Explicit-content handling (REQUIRED — never skip)

Threads sometimes contain explicit sexual roleplay. Handle every such thread as follows:

1. **Never reproduce, quote, or translate the explicit message** into the card, the report, or anywhere. Score the thread from its OUTCOMES and CONVERSATION STRUCTURE only (who escalated, did a sale land, was a signal read).
2. **Determine who drove the escalation.** Did the chatter push further than the fan, or was the chatter matching / pulling back from a fan who was already there?
3. **If the CHATTER was the one going overly explicit** (pushing past where the fan was):
   - In the report, name that this happened on the **[fanname] thread** — fan's first name / display name ONLY, never the surrounding message text.
   - Quote **only the single offending word** the chatter used. One word. Not the phrase, not the sentence.
   - Example shape: `On the [fanname] thread you pushed past where he was and used "[word]" — dial that back.`
4. **If the FAN drove it** and the chatter matched or pulled back: no word is quoted, the chatter is NOT tagged as escalating, and it is scored as ordinary value-setting / voice.
5. This who-led-whom call is a judgment made by reading the thread every run. It is the single most important reason a human should glance at unattended drafts before they post.

## Data retrieval method

1. Resolve the account. Set the UTC window for the shift that just closed.
2. `listTransactions(account, type=chat_messages, startDate=<day>, limit=20)` — newest-first list of message sales with `createdAt` (UTC), `amount` (gross), fan name (VIP tags show as "🏆 VIP NAME"). This is the cheapest way to find which fans the chatter actually sold to. Bin by the UTC window; ignore sales just outside it (they belong to the adjacent shift).
3. For each in-window sale and any active two-way thread, `listChatMessages(account, chat_id, limit, order='desc', skip_users='all')`; page with `first_id=<oldest id from prior batch>`.
4. Exclude `isFromQueue:true` messages — those are scheduled auto-content, not live chatter typing. Karina graveyard/morning lists are dominated by a scheduled auto-mass at ~02:48 UTC; do not score it as engagement.
5. Count restricted words from the chatter's outgoing (`isSentByMe:true` / `fromUser.id == model uid`) messages only.
6. Earnings elsewhere: `getEarningsOverview` returns NET; gross = net / 0.8. Always pass explicit 4-digit years.

Helper scripts (shipped beside this file): `reduce.py` (parse saved thread JSON to clean time/sender/text lines; set MODEL_ID), `bin_window.py` (bin saved thread JSON by UTC window; edit bounds + MODEL). Large tool payloads auto-save to `/mnt/user-data/tool_results/` — process them with these, do not pull them into context.

## Rendering the GIF card

Use the generic renderer shipped beside this file: `render_scorecard.py`.

```
python3 render_scorecard.py <config.json> <out_basepath>
```

Write one JSON config per chatter, then call once each. Config schema:

```json
{
  "name": "Alyzha",
  "sub": "Karina  ·  Afternoon  ·  June 24",
  "pillars": [["Relationship building",18],["Value setting",18],["VIP funnel",19],["Avoids dead ends",16]],
  "overall": 71,
  "restricted": 0,
  "weakest": "Avoids dead ends",
  "threads": "threads read: TW · VIP john  ·  attribution by shift window",
  "footer": "LIVERICHMEDIA  ·  CHATTER SCORECARD  ·  JUN 24 AFTERNOON"
}
```

(Use real middle-dot characters in `sub`/`threads`/`footer`.) Pillar colours and the weakest-link colour are derived automatically from the scores — callers supply only label+score, so there is no separate weakest-colour field to get wrong. Output: `<out_basepath>.gif` (the deliverable) and `<out_basepath>.jpg` (preview — always view it to verify before sharing). Copy the GIF to `/mnt/user-data/outputs/` and `present_files` it. Slack posts text only; the GIF must be dragged in manually by a human.

## Coaching report (Jassy's tone)

Warm but direct. Open with "Hi [name]" — NEVER "Hey". Lead with a genuine win, then name the weakest pillar with its score and one red emoji, then ONE concrete fix with an example line in the creator's voice (Shantal: personal, first-name, proper sentences; Karina: lowercase bratty). Emojis at line ends only. No dashes in fan/Slack copy. No word "tap" (use click/choose). Keep it short. Tag the chatter with <@SlackID>. Apply the explicit-content rule above to anything you reference.

## Running as a per-shift routine

Three runs/day, 15 min after each shift closes (PHT): 7:15am (graveyard just ended), 3:15pm (morning ended), 11:15pm (afternoon ended). Each run scores ONLY the shift that just closed, on BOTH accounts — so two chatters, two cards, two reports per run.

Routine prompt (keep short, point here, don't restate method):
> Run the chatter scorecard for the shift that just closed (use the current PHT time to pick graveyard/morning/afternoon) on both Shantal and Karina. Follow the of-chatter-scorecard skill: pull the window's chat-message transactions, read the active threads, score the four pillars, count restricted words per the per-account lists, apply the explicit-content handling rule, render each chatter's GIF card, and post each coaching report to that chatter's management channel tagging the chatter. Present both GIFs in chat for manual upload.

**Caution for unattended runs:** the explicit-content who-escalated call and the pillar scoring are judgments made by reading live threads. An unattended direct-to-channel post has no one to catch a misread before six people see it. A human skim of the drafts before posting is strongly recommended; staging into one self-channel first is the safer default.

## Safety

Read-only against OnlyFans. Never sends anything to a fan. The only writes are Slack posts to internal management channels.
