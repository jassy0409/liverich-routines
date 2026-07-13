# Chatter Playbook — Team Setup Guide

This kit gives your team the full LRM Chatter Playbook: a training site (manual +
5 modules), fillable exams that auto-grade and post scores + coaching to Slack,
and a weekly routine that sends each chatter their module and personal exam link
automatically.

## What's in the kit

- `index.html` — chatter hub (send this link to your team)
- `managers.html` — manager hub (keep private; links the answer keys)
- `chatter-training-manual.html` — the foundation manual
- `module-1…5-*.html` — chatter editions, manager guides, exams
- `playbook.css` — shared styling
- `roster.json` — YOUR team config (edit this first)
- `.github/workflows/pages.yml` — auto-deploys the site to GitHub Pages

## Fastest path: let Claude do it

Open a Claude Code session connected to your GitHub and Slack, upload this kit
(or point Claude at the repo it lives in), and paste:

```
Set up this Chatter Playbook kit for my team.
1. Create a repo <me>/<team>-playbook and add all the kit files.
2. Rewrite roster.json for my team — I'll give you each chatter's name, model,
   shift, Slack member ID, and management channel. Set "site" to my Pages URL
   and "rotationStartMonday" to next Monday.
3. In every module-*-exam-chatter.html update the CONFIG block: my chatters,
   my Slack incoming-webhook URLs (keep them base64-encoded), and my models'
   voice rules in the VOICE constant. Update the exam links in index.html.
4. Push, then walk me through enabling GitHub Pages (Settings → Pages →
   Source: GitHub Actions) and allowing the branch under Settings →
   Environments → github-pages → Deployment branches.
5. Test: submit one exam, confirm the Slack score + coaching messages arrive.
6. Create a weekly routine named "Weekly Chatter Playbook module send" with
   cron 0 1 * * 1 and the weekly prompt from TEAM-SETUP.md, then test-run it
   to my DM.
```

## Manual path

1. **Create a repo** on GitHub → upload every file in this kit (keep the
   `.github/workflows/` folder structure).
2. **Edit `roster.json`** — your chatters, Slack member IDs (start with `U`),
   management channels, your Pages URL in `site`, next Monday in
   `rotationStartMonday`.
3. **Wire Slack** — create Incoming Webhooks at https://api.slack.com/apps
   (one per management channel). Base64-encode each URL and paste it into the
   `CONFIG` block near the bottom of every `module-*-exam-chatter.html`
   (`webhook:dec("<base64>")`). The webhooks in this kit are intentionally
   blank — without yours, exams still work but only show "Copy my results".
4. **Enable GitHub Pages** — repo Settings → Pages → Source: **GitHub
   Actions**. Then Settings → Environments → github-pages → Deployment
   branches → allow your branch. Re-run the failed workflow if needed.
5. **Send links** — chatters get `index.html`; each chatter's personal exam
   link is `module-N-exam-chatter.html?chatter=<key>`.

## The weekly routine

Cron (Monday 9:00 AM PHT; hour is UTC — adjust for your timezone):

```
0 1 * * 1
```

Prompt:

```
Weekly Playbook send. Follow exactly:
1. Read roster.json in the repo (git pull first). It defines the site URL, the
   5 modules, the rotation start date, and the chatter list.
2. Compute this week's module: weeks = floor((today UTC - rotationStartMonday)
   / 7 days); module = modules[weeks % 5].
3. For each chatter: reading = site + module.read, exam = site + module.exam +
   "?chatter=" + key.
4. Post ONE Slack message to that chatter's management channel (use channelId
   if present; otherwise resolve by name with slack_search_channels; if it
   can't be resolved, skip and note it). Tag the chatter with <@slackId> when
   set. Tone: warm but direct, open with "Hi [name]" (NEVER "Hey"), emojis at
   line ends only, no dashes, no word "tap". Content: this week's module name,
   the reading link, their personal exam link, a reminder the exam takes about
   10 minutes and their score plus coaching posts back to this channel
   automatically, and one encouraging line.
5. Post ONLY to internal management channels. Never post to fans, never to
   OnlyFans, never to channels not in the roster.
6. Reply with a short report: module week, who was messaged, who was skipped
   and why.
```

## House rules baked into the kit (don't remove them)

- Exams grade written answers in each model's voice; edit the `VOICE` constant
  per model but keep the standard.
- Coaching messages correct mistakes from the module answer keys automatically.
- Company lines the training enforces: stay on-platform, no guilt-tripping or
  pressure tactics, never promise more than you deliver, notes on every fan.
