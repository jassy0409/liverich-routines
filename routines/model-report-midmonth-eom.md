Today is a potential run day. First, check today's date.

If today is the 15th, run a MID-MONTH report covering the 1st through the 15th of the current month. Evaluate targets at half the monthly goal.
If today is the 30th, run an END-OF-MONTH report covering the full current calendar month. Evaluate targets at the full monthly goal.
If today is neither the 15th nor the 30th, stop immediately and produce no output.

On a run day, produce one self-contained tabbed HTML dashboard per model: Shantal Monique, and Karina Petrova (VIP + Free combined into one file with VIP/Free splits inside). Save each to the LRM outputs folder named by model, report type, and date.
Accounts:

Shantal: acct_508c667e12d24250b75ae3d990594010 (uid 4669068)
Karina VIP: acct_48be256caa4c484cbab6774a098c4edb (uid 221746288)
Karina Free: acct_bd0c6dda969f4631b02b3a9524fa44be (uid 364264020)

Monthly GROSS targets: Shantal $100,000, Karina $20,000 (VIP + Free combined). On the 15th, on-pace = half the target. Flag each model ON PACE / AHEAD / BEHIND against the day-of-month pace line, and populate the Action Plan tab with concrete steps only when BEHIND.

DO NOT INCLUDE CHATTER NAMED ARSEL 
Data to pull, all via the OnlyFans MCP, all real, full depth:

Earnings: getEarningsOverview per account (one call each, never aggregated). Report GROSS by dividing net by 0.8. Never report net. For Karina, pull VIP and Free separately then combine.
Daily earnings series per account for the line chart (real per-day, not modeled).
Fan metrics: getSubscriberMetrics (detailed=true) and statisticsOverview for fans and visitors. Show the real numbers: total active fans, new fans, renewed, paid, free, new followers, lapsed/deleted, and reach (profile visitors).
Messages: pull DM + mass performance. Message revenue (PPV + DM tips) is reported on its own Messages tab, since that is where the real sales happen.
Posts: listPosts with counters, real captions, real likes and comments. Posts do NOT carry PPV sales. Show engagement only, and flag tip-wall campaign posts with their tip amount; mark everything else as an engagement post. Never attach fake PPV revenue to posts.
Stories and highlights: real story stats (views, likes, replies) and highlight views. Engagement only, no revenue.
Always use four-digit years in every date parameter. PHT is UTC+8; convert windows correctly.

Dashboard build (match the approved design exactly):

One HTML file per model with clickable scrollable tabs: Overview, Earnings, Messages, Engagement, Fans, Top Posts, Stories, Action Plan.
Girly pink accent on the dark LRM background (#141216 base, #201c22 panels), round gradient avatars, mint for reach, gold footer. Both models use this same girly style.
Fully animated high-end charts: count-up stat numbers, draw-on glowing line charts, rising bars, sweeping donut, growing funnel. Charts re-animate on tab switch. Use OnlyFans-style chart layouts (gridlines, axis labels) inside the dark panels.
Charts required: daily gross earnings line (Overview + Earnings), revenue-split donut (Earnings), message-to-sale funnel (Engagement), new-subscribers-per-day bars and cumulative growth line (Fans, dual VIP/Free bars for Karina), top-posts-by-likes bars (Top Posts), story-views bars (Stories).
No dash symbols anywhere in copy. Emojis only at line ends. Never use the word "tap" (use "click" or "choose").

After saving the files, post a short text summary to Slack: Shantal to #shantal-team (C09P2UMSE2G), Karina to #karina-team-reports (C0B38BXSM88). Each message leads with the pace status and percent of goal, and notes that the full animated dashboard HTML file is saved in the outputs folder, since Slack posts text only and files are added manually.
