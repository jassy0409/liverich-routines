Build and post the daily earnings recap for BOTH Shantal and Karina to Slack, each to her own team channel, as an animated GIF report card (NO Slack Canvas, do not create a canvas). Run every morning. This prompt is self contained. Work through the OnlyFans MCP connector (real numbers) and Slack (post AS Jassy, the authorizing user, in Jassy's plain warm voice, never a bot persona). Do both models in order, Shantal first then Karina. If one model's data pull, render, or post fails, still complete the other and note what failed at the end; never post a broken or guessed recap.

REPORTING WINDOW (critical, never change)
A sales day equals one full UTC calendar day, from T00:00:00Z to T23:59:59Z (this is the 8am PHT to 8am PHT window, since 8am PHT equals 00:00 UTC). Report the most recently completed full UTC calendar day. This routine runs every morning around 9am PHT, which is 01:00 UTC, so the day you report is "yesterday" in UTC (the local PHT date minus one). For example, running on the morning of June 19 PHT, report June 18. For each model pull start_date = the target day at T00:00:00Z and end_date = the target day at T23:59:59Z, and also pull the day before the target (same UTC window) to show the day over day change. Do not use PST or any other timezone to pick the day.

ALWAYS REPORT GROSS
Always report GROSS earnings (the full amount fans paid before OnlyFans takes its 20 percent fee). Never report net. If a tool gives net, convert to gross (net divided by 0.8) or use the gross field. Prefer getEarnings (type=total, messages, tips) which reports an explicit gross field that reconciles (messages gross plus tips gross equals total gross). getEarningsOverview is a cross check only; if they differ, trust the getEarnings gross field.

RENDER THE GIF REPORT CARD (required, this replaces the old canvas)
Use the renderer shipped beside this prompt: render_recap.py. It draws a dark LRM card in the same visual language as the chatter scorecard: a big animated gross figure in a 3D block that counts up, a day over day trend chip and paired trend bars, and a messages vs tips breakdown chart. Per model, write one JSON config and run:

  python3 render_recap.py <config.json> <out_basepath>

Config schema:
{
  "model": "Shantal",
  "sub": "June 18 2026",
  "gross_total": 1715,
  "prev_total": 1520,
  "messages_gross": 1310,
  "tips_gross": 405,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUN 18 2026"
}

Use real middle dot characters in sub and footer. messages_gross plus tips_gross must reconcile to gross_total. prev_total is the previous UTC day's gross total. The change percent, the trend colour (green when up, red when down, amber when flat), and the day over day bars are all derived automatically from gross_total vs prev_total, so there is no colour or percent field to set. After rendering, confirm the .gif exists on disk, view the .jpg preview to check it rendered correctly, then copy the .gif to /mnt/user-data/outputs/ and present it with present_files so Jassy can download it. This is a required deliverable per model. If a render fails, stop for that model and report the error rather than posting without a card.

MODEL 1: SHANTAL
- Account: Shantal Monique, acct_508c667e12d24250b75ae3d990594010 (single page).
- Pull gross total, messages gross, and tips gross for the target UTC day, plus the gross total for the day before (for the trend). Build the JSON config and render the card per the section above.
- Post a message to #shantal-team (channel_id C09P2UMSE2G) with slack_send_message, friendly "just keeping you looped in" spirit. NO canvas and no canvas link. Put the headline numbers in the message as short prose (gross total, day over day change up or down with the percent, messages gross, tips gross) so the channel has the figures even before the GIF is attached. Tag: model Shantal <@U09PTMDSE2C>, chatters Jeffrey <@U06AJLM4JM7>, Aaliyah <@U09U798V24X>, Princess <@U0B5Y66UDAQ>, Trisha <@U08H7941KTN>. After posting, state which channel it went to so Jassy knows where to drop the matching GIF. Auto post, no review.

MODEL 2: KARINA (combine TWO pages)
- Accounts (sum both for every figure): paid "Karina Petrova" acct_48be256caa4c484cbab6774a098c4edb, and free "Karinia Free" acct_bd0c6dda969f4631b02b3a9524fa44be. Pull each metric for BOTH and add paid plus free (gross total, messages gross, tips gross, and the prior day total). Build the JSON config from the COMBINED figures and render the card.
- Post a message to #karina-team-reports (channel_id C0B38BXSM88, private) with slack_send_message, "just keeping you looped in" spirit. NO canvas. Put the combined headline numbers in the message as short prose. Tag: model Karina <@U0B27P2UAPM>, chatters Leigh <@U0AHFGZ5ZM2>, Jeffrey <@U06AJLM4JM7>, Rossana <@U0AV2KV1DUG>, MJ <@U06ALHQ6PUH>. Do NOT tag Princess <@U0B5Y66UDAQ> (different model's team). After posting, state which channel it went to for the GIF drop. Auto post, no review.

OUTPUT — per model, two parts (mirror the chatter scorecard):
PART 1, the Slack message (AUTO-POST, text only, no canvas): the looped-in note with the headline gross numbers and the tags above.
PART 2, the GIF (do NOT auto-send, the Slack connector cannot attach image files): present the .gif here for Jassy to download and drag into the channel manually.

STYLE RULES (both models)
- No dash symbols anywhere in visible text (no hyphen, en dash, or em dash). Rewrite to avoid them (write "day over day", "8am PHT to 8am PHT").
- At most one or two emojis total per model.
- The note to each model must VARY every single day: fresh, natural, conversational, reacting to that day's real numbers. Never templated or robotic.
- Keep model facing notes non explicit and on brand. Money like $2,000.

After posting, report back which channels the two messages went to, confirm both GIFs were rendered and presented, and note any model that failed.
