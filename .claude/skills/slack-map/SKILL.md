---
name: slack-map
description: Show the Slack channels for each creator (model) team and the management channels, with channel IDs. Use when asked for the Slack map, which channel goes with which creator, or where a report should be posted.
---

# /slack-map

Show the Slack channel map for the workspace.

## Steps

1. Load the tools if needed: `ToolSearch` with `select:mcp__Slack__slack_search_channels`.
2. For any creator or channel not in the map below, run `mcp__Slack__slack_search_channels` with one keyword (the creator's first name or a team word) to check whether it has a channel now.
3. Present the result as a table with columns: Team, Channel, Channel ID, Type (public or private).
4. Say which creators have no channel found yet, and do not guess a channel name.

## Current map (checked 2026-11-19)

| Team | Channel | Channel ID | Type |
|---|---|---|---|
| Shantal Monique | #shantal-team | C09P2UMSE2G | private |
| Shantal Monique | #shantal-reports | C09PTMA9XLG | private |
| Karina Petro / KarinkaPetro | #karina-team-reports | C0B38BXSM88 | — (from the team's channel list; not found by search) |
| Staff | #management-team | C06A6KA0YCT | private |

## Shantal team chatters (shift in PHT)

| Chatter | Shift (PHT) | Slack User ID | Management channel |
|---|---|---|---|
| Aaliyah | Graveyard 11pm–7am | U09U798V24X | C09U784EE23 |
| Trisha | Morning 7am–3pm* | U08H7941KTN | C08FFLCF92N |
| Jeffrey | Midshift 3pm–11pm* | U06AJLM4JM7 | C08488V3C2G |
| Marianne | Cover (Trisha off-days + Aaliyah off) | no Slack ID on file | not set |

*Rotation trial started Nov 14: Jeffrey on morning, Trisha on midshift. Aaliyah stays on graveyard. Re-check this table if the trial ends.

## Rules

- "Model" means an OnlyFans creator whose page is managed. It never means a manager, a staff member, or an AI model.
- Before posting to any channel the user did not name, read its topic and description with `slack_search_channels`. If the description says that kind of message belongs elsewhere, tell the user instead of posting.
- This skill only lists channels. It does not post, read messages, or change anything.
