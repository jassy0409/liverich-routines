// LRM response generator backend (Vercel serverless function).
// Holds the Anthropic API key server-side. The browser never sees it.
// Requires a shared team password so random visitors can't spend your balance.

const PROMPTS = require("./_prompts.js");

module.exports = async (req, res) => {
  // CORS for same-origin use; tighten if you host the pages elsewhere.
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Use POST" });

  const KEY = process.env.ANTHROPIC_API_KEY;
  const TEAM_PASSWORD = process.env.TEAM_PASSWORD;
  if (!KEY) return res.status(500).json({ error: "Server missing ANTHROPIC_API_KEY" });
  if (!TEAM_PASSWORD) return res.status(500).json({ error: "Server missing TEAM_PASSWORD" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  const { password, model, fanMsg, scenario, context } = body || {};

  // Gate: reject anyone without the shared password.
  if (password !== TEAM_PASSWORD) {
    return res.status(401).json({ error: "Wrong or missing team password." });
  }

  const system = PROMPTS[model];
  if (!system) return res.status(400).json({ error: "Unknown model. Use 'shantal' or 'karina'." });
  if (!fanMsg || !fanMsg.trim()) return res.status(400).json({ error: "Empty fan message." });

  const userPrompt =
    `Fan's message: "${String(fanMsg).trim()}"\n` +
    `Scenario: ${scenario || "Other"}\n` +
    (context ? `Extra context: ${context}\n` : "") +
    `\nGenerate 2-3 response options to copy-paste. Plain text only, no markdown. ` +
    `If this is a complaint, refund, suspicion, frozen fan, or SVIP-number territory, ` +
    `output the escalation steps instead of a sales reply.`;

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-6",
        max_tokens: 1000,
        system,
        messages: [{ role: "user", content: userPrompt }],
      }),
    });
    const data = await r.json();
    if (!r.ok) {
      return res.status(r.status).json({ error: data?.error?.message || "Upstream error" });
    }
    const text = (data.content || [])
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("\n") || "No response generated.";
    return res.status(200).json({ text });
  } catch (e) {
    return res.status(500).json({ error: "Request failed. Try again." });
  }
};
