Build and post the daily earnings recap for BOTH Shantal and Karina to Slack, each to her own team channel. Run every morning. This prompt is self contained. Work through the OnlyFans MCP connector (real numbers) and Slack (post AS Jassy, the authorizing user, in Jassy's plain warm voice, never a bot persona). Do both models in order, Shantal first then Karina. If one model's data pull or post fails, still complete the other and note what failed at the end; never post a broken or guessed recap.

REPORTING WINDOW (critical, never change)
A sales day equals one full UTC calendar day, from T00:00:00Z to T23:59:59Z (this is the 8am PHT to 8am PHT window, since 8am PHT equals 00:00 UTC). Report the most recently completed full UTC calendar day. This routine runs every morning around 9am PHT, which is 01:00 UTC, so the day you report is "yesterday" in UTC (the local PHT date minus one). For example, running on the morning of June 19 PHT, report June 18. For each model pull start_date = the target day at T00:00:00Z and end_date = the target day at T23:59:59Z, and also pull the day before the target (same UTC window) to show the day over day change. Do not use PST or any other timezone to pick the day.

ALWAYS REPORT GROSS
Always report GROSS earnings (the full amount fans paid before OnlyFans takes its 20 percent fee). Never report net. If a tool gives net, convert to gross (net divided by 0.8) or use the gross field. Prefer getEarnings (type=total, messages, tips) which reports an explicit gross field that reconciles (messages gross plus tips gross equals total gross). getEarningsOverview is a cross check only; if they differ, trust the getEarnings gross field.

MODEL 1: SHANTAL
- Account: Shantal Monique, acct_508c667e12d24250b75ae3d990594010 (single page).
- Create a Slack Canvas (slack_create_canvas) titled with a comma not a dash, for example "Shantal Daily Recap, June 18 2026". Canvas content:
  - A short warm note addressed to Shantal, using the canvas user card ![](@U09PTMDSE2C) on its own line.
  - A Markdown TABLE: columns Metric, Amount; rows Gross total, Change vs day before (percent up or down), Messages (gross), Tips (gross).
  - One short honest closing line of encouragement.
- Post a message to #shantal-team (channel_id C09P2UMSE2G) with slack_send_message, friendly "just keeping you looped in" spirit, linking the canvas. Tag: model Shantal <@U09PTMDSE2C>, chatters Jeffrey <@U06AJLM4JM7>, Aaliyah <@U09U798V24X>, Princess <@U0B5Y66UDAQ>, Trisha <@U08H7941KTN>. Auto post, no review.

MODEL 2: KARINA (combine TWO pages)
- Accounts (sum both for every figure): paid "Karina Petrova" acct_48be256caa4c484cbab6774a098c4edb, and free "Karinia Free" acct_bd0c6dda969f4631b02b3a9524fa44be. Pull each metric for BOTH and add paid plus free (gross total, messages gross, tips gross, and the prior day totals).
- Create a Slack Canvas titled like "Karina Daily Recap, June 18 2026" (comma, no dash). Canvas content:
  - A short warm note addressed to Karina, using the canvas user card ![](@U0B27P2UAPM) on its own line.
  - A Markdown TABLE: columns Metric, Amount; rows Gross total, Change vs day before (percent), Messages (gross), Tips (gross). These are the COMBINED paid plus free figures.
  - One short honest closing line.
- Post a message to #karina-team-reports (channel_id C0B38BXSM88, private) with slack_send_message, "just keeping you looped in" spirit, linking the canvas. Tag: model Karina <@U0B27P2UAPM>, chatters Leigh <@U0AHFGZ5ZM2>, Jeffrey <@U06AJLM4JM7>, Rossana <@U0AV2KV1DUG>, MJ <@U06ALHQ6PUH>. Do NOT tag Princess <@U0B5Y66UDAQ> (different model's team). Auto post, no review.

STYLE RULES (both models)
- No dash symbols anywhere in visible text (no hyphen, en dash, or em dash). Rewrite to avoid them (write "day over day", "8am PHT to 8am PHT"). The only exception is the markdown table delimiter row.
- At most one or two emojis total per model.
- The note to each model must VARY every single day: fresh, natural, conversational, reacting to that day's real numbers. Never templated or robotic.
- Keep model facing notes non explicit and on brand. Money like $2,000.

After posting, report back both canvas links and both posted message links, and note any model that failed.
