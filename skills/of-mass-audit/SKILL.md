---
name: of-mass-audit
description: Build the full LiveRichMedia mass-message audit (Kylie-depth) for any OnlyFans creator via the OnlyFans API MCP server. Produces a self-contained dark-mode HTML report with bottom-line revenue YoY, monthly mass revenue + median-views charts, paid/free send counts, top earners, re-send winners, best days/times, price bands, and the full message log. Use when a manager says "run mass audit for [model]", "mass message report for [model]", "how is [model]'s mass messaging doing", "why is [model] dropping", or "Kylie-style report for [model]". Combines a creator's free + VIP pages into one report. Requires the OnlyFans API MCP connector.
---

# OF Mass Message Audit (full report)

Produce the full mass-message audit for one creator. NEVER fabricate a number — every
figure must come from an API response received in this session. If something can't be
pulled, say so; never ship zeros as data.

## Money rules (critical — get the numbers right)

1. `getEarningsOverview` returns **payout basis** (net of OnlyFans' 20%). Always label it
   "net of OnlyFans' 20% (payout basis)" AND show the dashboard equivalent (× 1.25) so
   models comparing against their own OF Statistics screen see matching numbers.
2. Verify category sums: subscriptions + posts + messages + tips + streams must equal
   total_earnings to the penny. If not, re-pull before using.
3. Mass revenue per message = price × purchasedCount = **list-price estimate** (overstates
   when fans buy at discounts). Label "est.". The `massMessagesChart`
   `group_messages_purchases` daily series is actual purchase dollars — use it to
   cross-check window totals (est. typically runs 0–25% above; note the gap).
4. Paid vs free: use the `isFree` flag, not price presence.
5. "Messages" in earnings ≠ mass messages. It includes 1-on-1 chatter DM unlocks. Mass
   endpoints capture ALL masses (manager full-list blasts AND chatter segment sends —
   segment sends have small sentCounts). Chatter 1-on-1 DMs are NOT masses.
6. Median views chart = full-list sends only: filter sent > 20% of the account's max
   sentCount; state the threshold in the chart subtitle.

## Pipeline (per model)

### Step 1 — Resolve accounts
`listAccounts` (response overflows to a file; Grep it for the username). Combine the
creator's free + VIP pages into ONE report. If the same username is connected twice,
use the newest account ID. If the API returns 401 SESSION_EXPIRED, report that the
account needs re-auth in the OnlyFansAPI dashboard and stop.

### Step 2 — Earnings frame (fast)
`getEarningsOverview` with all the model's account_ids in one array, twice:
Jan 1 → today's date for the current year, and the same window last year.
Record total + categories for both. Apply money rules 1–2.

### Step 3 — Message-level pull (the heavy part — use parallel agents)

**CACHE FIRST (cost control — mandatory).** Before pulling anything, fetch the cache
branch of jassy0409/liverich-routines (`git fetch origin claude/gracious-knuth-dwvodr`)
and look for `data/mass-audit/{slug}_mass.json` + `{slug}_meta.json`. If present:
- Re-pull ONLY from (meta.refresh_from = today − 90 days) forward. purchasedCount on
  masses older than ~90 days is effectively frozen, so cached records before that line
  are kept as-is; records inside the refresh window are replaced by the fresh pull
  (dedupe by date+price, fresh wins).
- Records older than the cache's coverage start (rare: first YoY run on an old page)
  still need a one-time historical pull for the missing range only.
- If no cache exists, this run seeds it: do the full historical pull below, then Step 4
  writes the cache. Expect full cost once; every later run costs only the 90-day window.

Endpoint `getMassMessageOverview` (account, limit 50–100, startDate, endDate,
"Y-m-d H:i:s"). Responses ALWAYS overflow to a host file (media bloat) — expected.
Extract per page with Grep (output_mode content, -o, head_limit 0), pattern:

    "date":"[^"]+","responseType"|"rawText":"(?:[^"\\]|\\.){0,70}|"isFree":(?:true|false)|"viewedCount":\d+,"sentCount":\d+|"price":"[\d.]+","purchasedCount":\d+

Matches stream in document order; each record starts at a date+responseType match;
price/purchasedCount appear only on paid sends; media objects never match these patterns.
Paginate via `_pagination.next_page` endDate cursor until hasMore=false.

CAPACITY RULE (measured): one agent carries ~1,500–1,800 records max. First estimate
cadence from a small probe or Step 2's chart counts, then split the 18-month window so
each pull agent stays under the cap (~3 sends/day → 6-month windows; ~10/day → 2-month;
~25/day → 1-month). Launch pull agents IN PARALLEL (model: opus). Each writes one JSON
array {date, sent, viewed, price|null, purchases|null, caption ≤70 chars} and reports
pages/records/paid/free/range/PASS-FAIL (+resume cursor if partial; partial = FAIL,
relaunch that window).

### Step 4 — Merge + build
Merge cached records (outside the refresh window) with all fresh window files: dedupe
by (date, price) with fresh records winning; enrich each record with day, month,
dow, hour, revenue = (price or 0) × (purchases or 0), paid = (price is not None); sort
by date; save {slug}_mass.json.

**WRITE THE CACHE BACK (mandatory).** Commit the merged {slug}_mass.json plus
{slug}_meta.json ({"slug", "account_ids", "coverage_start", "coverage_end",
"pulled_at", "refresh_days": 90}) to `data/mass-audit/` on branch
`claude/gracious-knuth-dwvodr` of jassy0409/liverich-routines and push. NEVER commit
this data to `main` or `claude/onlyfans-chat-guide-070tsw` — both trigger the public
GitHub Pages deploy and would publish revenue data. Then run scripts/build_full_report.py — edit its input
path, model name, usernames, subtitle record count, earnings card values (apply money
rules), and output path /Users/.../Downloads/{slug}-mass-message-audit-{date}.html.
New pages with no prior-year data: drop the YoY sections and 2025 chart rows; label
"new page — no prior-year baseline".

### Step 5 — Verify (mandatory before claiming done)
Python HTMLParser tag balance clean; zero `<script` tags; count of `<div class="msg`
rows == merged record count; bar div count == expected (12+6 monthly ×2 charts + 2 YoY
+ 7 day-of-week + 5 time-of-day = 50; fewer for new pages); earnings figures present
verbatim; zero references to other models. Report PASS/FAIL with evidence.

## Report sections (locked LRM design — do not restyle)

1. Brand header (LiveRichMedia gradient wordmark) + pulled date
2. "The bottom line first" — total revenue cards both windows (net label + ×1.25
   dashboard note), category deltas, mass-window est. revenue callouts, verdict warn-box
3. Mass vitals stat cards
4. Monthly est. mass revenue chart — pure CSS bars, one row per year, SHARED scale
5. Median views per full-list send chart (same pattern, threshold in subtitle)
6. Month-by-month table: masses / paid / free / est. rev / buys / median views
7. Top 10 earning masses
8. YoY same-window stat grid + 2-bar chart
9. "Proof re-sends print money" — up to 20 repeated-caption groups (normalize caption:
   lowercase, alnum+space, first 45 chars; ≥2 distinct days; rank by total revenue)
10. Best days & times — $ per paid send by day-of-week and time bucket
11. Price points that sell — bands <$10 / 10–15 / 15–20 / 20–30 / 30–50 / 50–100 / $100+
12. Playbook comparison (computed claims only)
13. Full message log — every record, grouped by month, newest first, color-coded
    (green = paid ≥$500 earned, blue = paid, gray = free)
14. Closing warn-box + summary box, footer tagline (never name vendors)

## Bundled scripts

- scripts/build_full_report.py — the gold-standard builder (working example wired for
  Lucy; adapt the input path / names / earnings constants per Step 4).

## Known findings to sanity-check against (June 2026 baseline)

Roster mass purchases Jan 1–Jun 3: 2025 $953.7k → 2026 $915.9k (−4.0%). Patterns seen:
view collapse follows volume spikes (send less → opens recover); $20–50 band earns most
per send; re-sent winning captions reliably sell again; "account up, broadcasts down"
means chatter DMs are masking a broadcast leak.
