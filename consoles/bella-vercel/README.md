# Bella Console — deploy in ~3 minutes

A private web app for the Erzabel chat team. Your Anthropic API key stays server-side; chatters never see it. Access is gated by a shared team password.

## Deploy to Vercel

1. Go to https://vercel.com/new → "Deploy" → drag this whole folder in
   (or: `npm i -g vercel` then run `vercel --prod` inside this folder).
2. In the Vercel project → Settings → Environment Variables, add:
   - ANTHROPIC_API_KEY  → your key from https://console.anthropic.com
   - TEAM_PASSWORD      → any shared password for the chatters
3. Redeploy (Deployments → ⋯ → Redeploy) so the env vars take effect.
4. Share the URL (e.g. https://bella-console.vercel.app) + password with the team.

## Files
- index.html      — the console UI
- api/generate.js — serverless route: password check + Anthropic call + persona rules
- vercel.json     — noindex headers so search engines never list it

## Notes
- Model: claude-sonnet-4-5 via the Messages API.
- To change the password or key, edit the env vars — no code change needed.
- To update persona rules or price floors, edit PERSONA_PROMPT in api/generate.js and redeploy.
