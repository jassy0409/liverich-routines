# LiveRichMedia scheduled routines

Paste-ready prompt text for each scheduled routine (one file per routine).
The scheduler API cannot edit a routine prompt body, so updates are applied by
pasting the matching file into the routine.

Roster note: afternoon 3pm-11pm shift changed. Arsel (Shantal) replaced by
Princess (#princessf-management C0B5D3AJYB1, U0B5Y66UDAQ); Alyzha (Karina)
replaced by Rossana (#rosanna-management C0AUM8Z0SSD, U0AV2KV1DUG).

| Routine | File | Cron | Trigger ID | Roster status |
|---|---|---|---|---|
| CHATTER SCORECRAD | [chatter-scorecard.md](chatter-scorecard.md) | `15 7,15,23 * * *` | `trig_01FKPqYkLPdVQH28ypF6dbWq` | updated (Princess/Rossana already applied) |
| SHIFT GOAL CHECKER | [shift-goal-checker.md](shift-goal-checker.md) | `0 */2 * * *` | `trig_01VXQpXrAGYCiEV5hPCLrBVU` | no roster refs |
| hand off shift reporter DAILY | [shift-handoff-reporter.md](shift-handoff-reporter.md) | `15 7,15,23 * * *` | `trig_01WsaCKdunzKyBUU3aqSdb8a` | updated: Arsel→Princess, Alyzha→Rossana |
| MODEL REPORT MID MONTH AND EOM SALES REPORT | [model-report-midmonth-eom.md](model-report-midmonth-eom.md) | `0 9 15,30 * *` | `trig_01TvSFKieBHbAcabEPMM8u19` | no roster refs |
| huddle chatter checker | [huddle-chatter-checker.md](huddle-chatter-checker.md) | `59 * * * *` | `trig_01MyuFDMvNEVsSvgVydxyXsR` | updated: Arsel→Princess, Alyzha→Rossana |
| chatter queue auto eply | [chatter-queue-autoreply.md](chatter-queue-autoreply.md) | `30 * * * *` | `trig_012VCP1bfpWneuQbGtMEV79r` | no roster refs |
| BUMP REQUEST SHANTAL+KARINA | [bump-request-shantal-karina.md](bump-request-shantal-karina.md) | `1 * * * *` | `trig_01Y6FExGTxxcKiP2UGxJzjDE` | no roster refs |
| DAILY RECAP (SHANTAL+KARINA) | [daily-recap-shantal-karina.md](daily-recap-shantal-karina.md) | `0 1 * * *` | `trig_01Cf6oy9NbWGDfkVVvxqKKDC` | updated: roster swap + Canvas replaced by animated `render_recap.py` GIF card |
| CHATTER SHIFT CHECKER | [chatter-shift-checker.md](chatter-shift-checker.md) | `59 * * * *` | `trig_01S1x5ed1DUJJP7uuyppp4Vu` | no roster refs |
