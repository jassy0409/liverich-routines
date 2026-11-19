---
name: of-models
description: List every OnlyFans creator ("model") in this workspace with their username and creator ID. Use when asked for all models, all creators, or which creators are set up.
---

# /of-models

List all creators (models) in the workspace.

## Steps

1. Load the tool if needed: `ToolSearch` with `select:mcp__SuperCreator__list_creators`.
2. Call `mcp__SuperCreator__list_creators` with no arguments.
3. Present the result as a table with columns: Creator, Username, Creator ID.
4. Add one line noting the list comes from SuperCreator and shows only the creators that tool can see.

## Rules

- "Model" means an OnlyFans creator whose page is managed. It never means a manager, a staff member, or an AI model.
- Show only the name, username, and creator ID. Do not add earnings, fan data, or contact details unless the user asks for them in a separate request.
- Do not show any email address.
