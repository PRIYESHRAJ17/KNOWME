# KNOWME

**One context graph. One user-defined rulebook. One audit trail.**

KNOWME is a proposed personal-context layer for everyday AI. It aims to connect a person's routines, memories and authorised data so assistance can be personalised, permission-aware and auditable.

**Initial focus:** older adults and family caregivers.  
**Product direction:** phone-first companion with an optional clip-on concept.  
**Team:** Knight Rebels  
**Track:** wHACKiest 2026 – Track 03, Know Thyself  
**Team ID:** `bbc1f678`

## What this repository contains today

This repository starts with a small, runnable backend framework demonstrating the central KNOWME workflow:

1. Save an evidence-linked memory.
2. Check the user's permission policy.
3. Request approval when required.
4. Record the action decision and a demo action receipt.

### Implemented in this starter

- FastAPI backend with interactive API documentation.
- SQLite local persistence.
- Create and list memories with source, domain, confidence and optional expiry.
- User permission policies with `allow`, `ask` and `deny` decisions.
- Reminder request workflow with approval gating.
- Action history and demo receipts.

### Planned; not implemented in this starter

- ElevenLabs Scribe speech-to-text and Turbo text-to-speech integration.
- AWS deployment using ECS Express Mode, RDS PostgreSQL/pgvector, S3 and KMS.
- Mobile app, wearable hardware and Bluetooth integration.
- Real phone notifications, family messaging and external agent integrations.

The reminder flow currently records a request in the local database. **It does not create an actual phone alarm or send a notification.** The voice and AWS services are architectural plans, not integrations claimed as complete.

## Run locally

Requirements: Python 3.10 or newer.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app:app --reload
```

If PowerShell blocks virtual-environment activation, run the app using the environment's executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000/docs** to try the API. The local SQLite database is created automatically as `knowme.db`.

## Quick demo flow

Use the interactive docs at `/docs`:

1. `POST /memories` – add a synthetic memory, for example `Medicine dose updated after clinic visit`, with source `Sample visit note` and domain `health`.
2. `GET /memories` – confirm the memory and its source are stored.
3. `GET /permissions` – inspect the default policy. `create_reminder` defaults to `ask`.
4. `POST /actions/reminders` – request a reminder and include the memory ID. The API should return `pending_approval`.
5. `POST /actions/{action_id}/approval` – approve the action by sending `{"approved": true}`.
6. `GET /actions` – inspect the resulting action receipt.

Use synthetic information only. This is a software demonstration, not a medical device or clinical decision system.

## Repository map

```text
KNOWME/
├── README.md
├── docs/
│   └── architecture.md
├── app.py
├── requirements.txt
├── .gitignore
└── .env.example
```

## Technology direction

| Layer | Current starter | Planned direction |
|---|---|---|
| API | FastAPI | FastAPI |
| Local storage | SQLite | Amazon RDS PostgreSQL + pgvector |
| Voice | Not connected | ElevenLabs Scribe + Turbo TTS |
| Cloud | Local development | AWS ECS Express Mode, S3 and KMS |
| Policy | Basic local rules | Expanded Context Firewall and audited approvals |

## Security notes

- Do not commit `.env`, API keys, AWS credentials or personal records.
- `.env.example` contains placeholders only.
- Use synthetic data in demos and tests.
- Review every external integration for consent, data retention and least-privilege access.

## Status

**Starter MVP framework – local workflow implemented; voice, cloud deployment, mobile UI and hardware integrations are planned.**
