# LiveRich Chatter Console (AI version)

One console, three models (Shantal · Karina · Bella), two tabs (Fan reply · PPV/Caption studio).
Every request sends `SYSTEM_PROMPT.md` + `MODELS_MASTER_DATASHEET.md` to Claude, so drafts follow
each model's voice, pricing floors, hard-block words, VIP protections and escalation rules.

## Option A — Claude Project (no code, works today)

1. On claude.ai, create a Project per model (e.g. "Shantal Console").
2. Paste `SYSTEM_PROMPT.md` as the project's custom instructions, replacing the MODEL line
   with that model's name.
3. Upload `MODELS_MASTER_DATASHEET.md` to the project's knowledge files.
4. Invite the chatters to the Project. They paste fan messages, prefix `MODE: caption` for Tab 2.

## Option B — Vercel deploy (branded URL, no Claude accounts needed)

1. `cd consoles/ai && vercel deploy` (or import this folder as a Vercel project from GitHub,
   set the Root Directory to `consoles/ai`).
2. In Vercel → Settings → Environment Variables, add:
   - `ANTHROPIC_API_KEY` — from console.anthropic.com
   - `CLAUDE_MODEL` (optional) — defaults to `claude-sonnet-5`
3. Optionally enable Vercel password protection so only the team can open it.
4. Share the URL with chatters.

## Notes

- Update the datasheet by replacing `MODELS_MASTER_DATASHEET.md` and redeploying — the prompt
  reads it fresh on cold start.
- The static (no-AI) consoles remain in `consoles/*.html` as offline fallbacks.
