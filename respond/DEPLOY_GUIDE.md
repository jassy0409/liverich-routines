# LRM Response Generator - Deploy Guide

This gives your chatters ONE link. They open it, type the team password once, and generate live replies in Shantal's or Karina's voice. No chatter needs a Claude login. The link is safe to share because your API key stays on the server and a password blocks strangers.

You do NOT need to know how to code. Follow the steps.

## What this costs

Every "Generate" click calls the Claude API and costs you a small amount (fractions of a cent to a few cents per click, depending on length). Across a full team it can add up to a few dollars to tens of dollars a month. You pay Anthropic directly for API usage. This is separate from your Claude.ai subscription. Check current pricing at console.anthropic.com.

## What you need (three accounts, all free to create)

1. An Anthropic API account with billing added - console.anthropic.com
2. A Vercel account (free tier is fine) - vercel.com
3. A GitHub account (you already have one) OR you can upload straight to Vercel

---

## Step 1 - Get your Anthropic API key

1. Go to console.anthropic.com and sign in.
2. Add a payment method under Billing. Set a low monthly spend limit at first so there are no surprises.
3. Go to API Keys, click Create Key, copy the key (starts with sk-ant-...). Keep it somewhere safe. You paste it into Vercel later, never into the files.

## Step 2 - Put these files in a GitHub repo

Upload this whole folder (the `api` folder, the `public` folder, `vercel.json`, `package.json`) to a new GitHub repo, for example `lrm-response-generator`. Do NOT upload the two `.txt` files if they are present, they are not needed.

## Step 3 - Deploy on Vercel

1. Go to vercel.com, sign in, click Add New then Project.
2. Import the GitHub repo you just made.
3. Before clicking Deploy, open Environment Variables and add TWO:
   - Name: `ANTHROPIC_API_KEY`  Value: your sk-ant-... key from Step 1
   - Name: `TEAM_PASSWORD`  Value: a password you make up for your team (for example a phrase only your chatters know)
4. Click Deploy. Wait about a minute.
5. Vercel gives you a live URL like `https://lrm-response-generator.vercel.app`. That is the link you send your team.

## Step 4 - Test it yourself first

Open the Vercel URL in your own browser. Type the team password. Paste a fan message, pick a scenario, click Generate. You should get replies. Try a refund message too - it should return the escalation steps, not a sales line.

## Step 5 - Send it to your chatters

Send them the link and the team password (separately is safer). They type the password once and it is remembered on their device. Done. No Claude login needed.

---

## Keeping your money safe

- The password gate stops strangers. If the link leaks, change TEAM_PASSWORD in Vercel Environment Variables and redeploy - old password stops working.
- Set a spend limit in the Anthropic console so usage can never run past what you allow.
- If you ever think your API key leaked, roll it in the Anthropic console and update it in Vercel.

## Updating the voice or rules later

The models' voices and rules live in `api/_prompts.js`. To change them, come back to this chat, tell me the change, I regenerate `_prompts.js`, you replace that one file in the repo, and Vercel redeploys automatically. Do not hand-edit that file unless you are comfortable, it is one long line.
