# KNOWME – Initial Architecture

## Product idea

KNOWME is a proposed personal-context layer that connects a person's memories, routines and authorised data to permission-controlled assistance. The initial product focus is older adults and family caregivers, with a phone-first experience and an optional clip-on concept.

## Core loop

1. **Capture** – accept explicit user input first. Voice capture through ElevenLabs is a planned integration.
2. **Unify** – save a memory with its domain, source, confidence, timestamp and optional expiry in the LifeGraph.
3. **Govern** – check the user's policy for the requested action. The starter app supports `allow`, `ask` and `deny` decisions.
4. **Approve** – require a user decision when policy says `ask`.
5. **Act and record** – the starter app records a reminder request and produces an action receipt. It does not send an external notification.

## Current starter implementation

- FastAPI HTTP API with interactive docs at `/docs`.
- SQLite persistence for local development.
- Memory create/list endpoints.
- Permission list/update endpoints.
- Reminder request endpoint that checks the permission policy.
- Approval/denial endpoint that writes a demo action receipt.
- Action history endpoint.

## Planned integrations (not implemented in this starter)

- **ElevenLabs** – Scribe speech-to-text and Turbo text-to-speech.
- **AWS** – ECS Express Mode for hosting, RDS PostgreSQL with pgvector for persistent memory, S3 for user-authorised objects and KMS for key management.
- **Mobile app / wearable** – phone-first application, optional ESP32-S3 clip-on, Bluetooth Low Energy and physical microphone mute.
- **Agent tools** – scoped integrations, explicit approvals, outcome verification and recovery.

## Trust and safety boundaries

- Use synthetic demo data; do not upload real medical records or personal health information to this starter repository.
- A memory's source and confidence are stored separately from the memory text.
- Consequential actions should require explicit approval.
- The reminder action in this starter is a local database record only. No alarm, message, medical recommendation or external action is performed.
- Never commit API keys, AWS credentials or `.env` files.

## Local data model

- `memories`: content, domain, source, confidence, creation time and optional expiry.
- `permissions`: action type, user decision and update time.
- `actions`: requested action, schedule text, linked memory, status, approval timestamp and receipt.

## Next development milestones

1. Add automated tests for memory creation, policy decisions, approval and receipt integrity.
2. Add ElevenLabs voice input/output behind a provider adapter.
3. Replace local SQLite with PostgreSQL when deploying to AWS.
4. Add a user interface for the LifeGraph, permission settings and action receipts.
5. Add scoped external integrations only after consent, approval and audit behaviour are tested.
