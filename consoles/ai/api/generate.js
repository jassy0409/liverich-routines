const fs = require("fs");
const path = require("path");

const MODELS = {
  shantal: "SHANTAL MONIQUE",
  karina: "KARINA PETROVA",
  bella: "ERZABEL (BELLA)",
};

let cachedPrompt = null;
function buildSystem(modelKey) {
  if (!cachedPrompt) {
    const dir = process.cwd();
    const prompt = fs.readFileSync(path.join(dir, "SYSTEM_PROMPT.md"), "utf8");
    const datasheet = fs.readFileSync(path.join(dir, "MODELS_MASTER_DATASHEET.md"), "utf8");
    cachedPrompt = { prompt, datasheet };
  }
  const name = MODELS[modelKey];
  return (
    cachedPrompt.prompt.replace(/\{\{MODEL\}\}|\{\{SHANTAL MONIQUE \| KARINA PETROVA \| ERZABEL \(BELLA\)\}\}/g, name) +
    "\n\n---\n\n# ATTACHED KNOWLEDGE FILE: MODELS_MASTER_DATASHEET.md\n\n" +
    cachedPrompt.datasheet
  );
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const { model, mode, input, fanName } = req.body || {};
  if (!MODELS[model]) return res.status(400).json({ error: "unknown model" });
  if (!input || !input.trim()) return res.status(400).json({ error: "empty input" });
  if (!process.env.ANTHROPIC_API_KEY) return res.status(500).json({ error: "ANTHROPIC_API_KEY not set" });

  const userMsg =
    "MODE: " + (mode === "caption" ? "TAB 2 — PPV / CAPTION STUDIO" : "TAB 1 — FAN REPLY") +
    (fanName ? "\nFan name: " + fanName : "") +
    "\n\n" + input.trim();

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": process.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: process.env.CLAUDE_MODEL || "claude-sonnet-5",
        max_tokens: 1600,
        system: buildSystem(model),
        messages: [{ role: "user", content: userMsg }],
      }),
    });
    const data = await r.json();
    if (!r.ok) return res.status(502).json({ error: (data && data.error && data.error.message) || "api error" });
    const text = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
    return res.status(200).json({ text });
  } catch (e) {
    return res.status(502).json({ error: "generation failed, try again" });
  }
};
