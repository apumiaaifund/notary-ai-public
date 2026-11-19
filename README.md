---
title: Notary AI
emoji: 🛡️
colorFrom: blue
colorTo: slate
sdk: docker
app_port: 7860
pinned: false
---

# Notary AI — Cryptographic Proof & Verification Node

Zero-dependency, memory-safe proof registry for AI agents.
- **Public Verification UI:** `GET /`
- **Verify API:** `GET /api/verify?q=<sha256_or_action_id>`
- **Chain Head Checkpoint:** `GET /api/head`
- **Stamp API (Protected):** `POST /api/stamp` (`Authorization: Bearer <NOTARY_API_KEY>`)
