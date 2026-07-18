# Mass-audit cache

Cost-control cache for the of-mass-audit skill. Each creator gets two files:

- `{slug}_mass.json` — the merged message-level history (Step 4 output): one record
  per mass send with date, sent, viewed, price, purchases, caption (<=70 chars).
- `{slug}_meta.json` — {"slug", "account_ids", "coverage_start", "coverage_end",
  "pulled_at", "refresh_days": 90}

How the audit uses it: records older than 90 days are read from here for free;
only the trailing 90-day window is re-pulled from the OnlyFans API (purchase counts
on older masses are effectively frozen). First audit after this was set up seeds
the cache at full cost; every later audit costs ~10-20 API calls instead of
hundreds.

PRIVACY: this branch (claude/gracious-knuth-dwvodr) is NOT deployed anywhere.
Never move these files to `main` or `claude/onlyfans-chat-guide-070tsw` — both
branches trigger the public GitHub Pages deploy.
