# Notary AI — Public Verification Protocol

Zero-PII cryptographic proof verification endpoint.

## Public Endpoints
- `GET /` — Minimalist web verification UI
- `GET /api/verify?q=<sha256_or_action_id>` — Instant O(1) proof lookup & WORM chain status
- `GET /api/head` — Current Merkle/WORM chain head checkpoint
