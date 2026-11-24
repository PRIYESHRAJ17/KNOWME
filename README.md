
##  Project Overview

**KNOWME** is a proposed, age-inclusive personal intelligence platform designed to bring a person's authorised information—memories, routines, goals, health and fitness signals, appointments, conversations, and commitments—into one source-linked personal context layer.

Instead of treating every app interaction as an isolated request, KNOWME builds a user-controlled understanding of relevant context over time, uses that context to provide meaningful assistance, asks for permission before consequential actions, and logs verifiable records of everything that happens.

While designed for everyone, our initial pilot focuses on **older adults and their families**. The long-term product is built to serve students, professionals, and individuals with accessibility needs.

| Attribute | Details |
| :--- | :--- |
| **Project** | **KNOWME** |
| **Team** | **Knight Rebels** (Team ID: `bbc1f678`) |
| **Hackathon** | **wHACKiest 2026** — *Track 03: Know Thyself* |
| **Team Members** | **Priyesh Raj** (Lead) • **Shrinidhi Hebbar P M** • **Shyam Swaroop N** |
| **Repository** | [https://github.com/PRIYESHRAJ17/KNOWME](https://github.com/PRIYESHRAJ17/KNOWME) |

---

## 📑 Table of Contents

- [1. The Problem We Are Addressing](#1-the-problem-we-are-addressing)
- [2. What We Are Building](#2-what-we-are-building)
- [3. The First End-to-End Experience](#3-the-first-end-to-end-experience)
- [4. Product Surfaces & Planned Technology](#4-product-surfaces--planned-technology)
- [5. Roadmap](#5-roadmap)
- [6. Proposed Pilot Success Measures](#6-proposed-pilot-success-measures)
- [7. Business Model Hypotheses](#7-business-model-hypotheses)
- [8. Privacy, Safety & Product Boundaries](#8-privacy-safety--product-boundaries)
- [9. Implementation Status](#9-what-is-implemented-in-this-repository-today)
- [10. Quickstart: Run Locally](#10-run-the-current-starter-locally)
- [11. Repository Structure](#11-repository-structure)
- [12. Development Principles](#12-development-principles)
- [License](#license)

---

## 1. The Problem We Are Addressing

Personal information today is fragmented across isolated silos: steps and activity on a phone, sleep data on a wearable, health history in medical records, appointments in calendars, and commitments inside chats or memory.

* A reminder knows the **time**, but has no idea **what changed in your day**.
* A generic AI assistant answers questions without disclosing **which data it used**, whether that data is **fresh**, or whether it had **consent** to touch or share it.

KNOWME directly addresses four systemic failures:

1. **Fragmented Context**: Personal details are scattered across disparate apps, services, and hardware.
2. **Lack of Continuity**: Existing tools fail to preserve continuity across evolving events, health changes, and follow-ups.
3. **Weak Personalisation**: Virtual assistants lack an evolving, correctable representation of a person's habits, preferences, and personal boundaries.
4. **Trust and Control Deficits**: Sensitive personal data lacks explicit provenance, confidence ratings, expiry windows, dispute resolution, and exportability.

> **Product Hypothesis:** Rather than adding another point solution, conversation capture, wearables, health insights, and task automation should converge through a **common personal context layer** governed by **enforceable, user-defined policies**.

---

## 2. What We Are Building

KNOWME is not just another chatbot, reminder app, or wearable. At its core is the **Personal LifeGraph**: a time-aware, graph-structured context layer containing verified personal facts and events, backed by explicit evidence of origin, confidence scores, and freshness.

The system operates across five core stages:

### `01 — Sense` (Opt-in Multi-modal Ingestion)
Ingests only user-authorised inputs:
* Explicit user voice and text input.
* Device data (calendar events, contacts, alarms).
* Health and fitness signals (e.g., via Android Health Connect).
* Optional connected wearables and the custom KNOWME clip-on device (engineered with a physical hardware mic-mute switch).

### `02 — Unify` (The Personal LifeGraph)
Converts raw inputs into a structured, temporal knowledge graph:
* Facts, episodes, and life events.
* People, social circles, and relationships.
* Routines, circadian rhythms, and recurring habits.
* Goals, active commitments, and pending tasks.
* Health, mobility, and activity metrics.
* *Every node retains source URI, timestamp, confidence level, freshness index, and optional user-defined expiry.*

### `03 — Govern` (Personal AI Constitution + Context Firewall)
Users define explicit operational policies for their data boundaries. Decisions are strictly triaged into three paths:
* **Allow**: The action satisfies saved policies and proceeds automatically.
* **Ask**: The system must explicitly request user confirmation before proceeding.
* **Deny**: The operation is immediately halted and logged.
* *Policies are granularly scoped by action type, sensitivity domain (Health, Family, Work, Finance), and recipient.*

### `04 — Orchestrate` (Provider-Independent Agent Runtime)
A decoupled agent orchestration runtime retrieves relevant LifeGraph subgraphs to answer questions or prepare actions. Model backends, STT/TTS services, and external tools are modular plugins rather than hardcoded dependencies. Consequential actions require explicit, interactive user approval.

### `05 — Verify` (Action Receipts & Audit Trail)
Following any approved action, KNOWME verifies external service outcomes (where supported) and generates an immutable **Action Receipt** detailing:
* Action triggered & target service
* Source context & retrieval provenance
* Permission decision & timestamped user approval
* Final execution status & undo/recovery options

---

## 3. The First End-to-End Experience

Our reference end-to-end user journey is intentionally narrow and explainable:

1. **Input:** A user shares a routine change (e.g., *"Doctor adjusted my evening walking schedule"*).
2. **Extraction:** KNOWME extracts the structured event and commits it to the LifeGraph with timestamp and source provenance.
3. **Inspection:** The user views, validates, or corrects the newly saved memory.
4. **Trigger:** The user requests: *"Set a reminder based on my new schedule."*
5. **Firewall Evaluation:** The Context Firewall evaluates the policy. As scheduling alters external state, it evaluates to `Ask`.
6. **Approval:** The user confirms the prompt via voice or UI.
7. **Execution & Receipt:** The action executes, generating a verifiable Action Receipt in the audit trail. Any family notifications require a separate, independent consent check.
Capture ──► Source-Linked Memory ──► Permission Check ──► User Approval ──► Action ──► Verifiable Receipt

> [!NOTE]
> Initial prototypes and public demonstrations rely exclusively on **synthetic test data**.
>
> **Medical Disclaimer:** KNOWME is not a medical device. It is not intended to diagnose medical conditions, prescribe treatments, or provide medication dosing instructions.

---

## 4. Product Surfaces & Planned Technology

KNOWME is **phone-first**. The custom clip-on is an optional convenience; no external hardware is required to access the core platform.

### Architecture Matrix

| Layer | Planned Direction | Role |
| :--- | :--- | :--- |
| **Optional Wearable** | ESP32-S3, INMP441 I²S microphone, BMI270 IMU, speaker/haptic driver, physical hardware mute switch | Ambient voice capture & motion signal streaming *(Hardware specs subject to pilot validation)* |
| **Mobile Application** | Flutter, BLE (Bluetooth Low Energy), Android Health Connect, SQLite/Hive local cache | Core user touchpoint, local consent management, accessible UI |
| **API & AI Runtime** | Python, FastAPI, Pydantic, temporal/entity parsers, provider-agnostic LLM interface | Business logic, semantic memory retrieval, and agent orchestration |
| **Voice Engine** | ElevenLabs Scribe v3 Live (STT) & v4 Turbo (TTS) | Low-latency conversational voice interface |
| **Cloud & Storage** | AWS ECS (Express Mode), RDS PostgreSQL with `pgvector`, S3, AWS KMS (*Mumbai `ap-south-1` Region*) | Scalable vector search, structured relational persistence, and encrypted document storage |
| **Agent / Tooling** | Model Context Protocol (MCP) adapters, scoped OAuth 2.0 PKCE, idempotent runners | Interoperable third-party integrations with strict permission gates |
| **Trust Control Plane** | Identity, consent registries, domain policies, cryptographic audit trail, data shredder | Strict enforcement of personal data boundaries and compliance |

### Local-First Cost Strategy
KNOWME targets a near-zero baseline operating cost using local-first computation, open-source storage primitives, and free-tier cloud architectures. Paid cloud APIs (LLMs, neural voice) are strictly rate-limited and user-configurable to prevent uncontrolled runtime expenses.

---

## 5. Roadmap

### Stage A — Core Demo *(Current Milestone)*
- Single complete, verifiable workflow on a mobile form factor.
- Phone UI featuring voice input and audio response.
- Source-linked memory ingestion and retrieval.
- LifeGraph node inspection with confidence and origin markers.
- Enforcement of `Allow`, `Ask`, and `Deny` rules.
- One fully gated, user-approved action execution.
- Verifiable Action Receipt rendering.

### Stage B — Alpha Pilot *(0–90 Days)*
- Supervised field trials with older adults and their immediate care circles.
- Retrieval-augmented generation (RAG) fine-tuning for conversational provenance.
- Validation of consent friction, multi-party sharing boundaries, and approval UX.
- High-contrast visual modes and voice accessibility optimisations.
- Quantitative tracking of task completion rates and token/infrastructure expenses.

### Stage C — Platform Maturity *(12–36 Months)*
- Decentralised/portable LifeGraph data export specs.
- Bi-directional sync across calendars, wearable ecosystems, and electronic health records.
- In-house ESP32-S3 clip-on companion device release.
- Care-circle delegation models with fine-grained RBAC.
- Developer MCP SDK and institutional APIs.
- Multilingual conversational capabilities targeting 15+ Indian languages and regional dialects, evaluated on a language-by-language basis.

---

## 6. Proposed Pilot Success Measures

The following empirical engineering benchmarks define our validation criteria for Stage A & B milestones:

| Success Measure | Proposed Target | Evaluation Methodology |
| :--- | :--- | :--- |
| **Personal Fact Retrieval** | **≥ 90%** | Accurate recall and provenance attribution across a curated 50-fact evaluation suite |
| **Policy Enforcement Accuracy** | **100%** | Strict compliance with `Allow` / `Ask` / `Deny` rules in synthetic unit & integration tests |
| **Zero Unauthorized Actions** | **0 Breaches** | Zero unapproved executions across 100 consecutive consequential action attempts |
| **Audit Receipt Integrity** | **≥ 95%** | Correctly generated, verifiable receipts for all executed actions |
| **Voice Task Success** | **≥ 90%** | End-to-end voice intent capture and task execution across two pilot languages |

> [!WARNING]
> Meeting these internal engineering benchmarks verifies software correctness; it does not constitute clinical efficacy, medical-grade compliance, or production certifications.

---

## 7. Business Model Hypotheses

KNOWME adopts a **freemium, privacy-first** monetization model:

* **KNOWME Core (Free):** Full phone-based personal context graph, local-first storage, essential firewall controls, and standard task management.
* **KNOWME Pro (₹1,999 / year):** Extended vector context retention, premium multi-modal LLM routing, high-fidelity neural voice quotas, and advanced third-party integrations.
* **Hardware Clip-on (~₹5,000 one-time):** Optional standalone microphone/haptic wearable for hands-free convenience.
* **Family & Care Circle Tier:** Granular multi-user access controls, shared calendars, and emergency escalation workflows.
* **Enterprise & Healthcare OEM:** Managed B2B APIs for elder-care providers, assisted living communities, and wellness organisations.

*Note: Pricing and unit economics are planning estimates subject to empirical revision during Stage B alpha trials.*

---

## 8. Privacy, Safety & Product Boundaries

Trust is an architectural invariant of KNOWME, not a secondary feature:

- **Explicit Opt-in:** Background listening is strictly opt-in. The clip-on hardware includes a mechanical physical mute switch that breaks the circuit to the microphone.
- **Domain Partitioning:** Personal information is isolated across logical domains (`Health`, `Family`, `Financial`, `General`). Cross-domain queries are blocked by default.
- **Explainable Uncertainty:** Memories contain explicit confidence metrics. When factual certainty is low, the agent abstains rather than halluncinates.
- **Mandatory Approval Gates:** Sensitive actions and cross-boundary data shares require explicit user consent.
- **Principle of Least Privilege:** Third-party integrations communicate via scoped OAuth tokens and constrained MCP interfaces.
- **User Ownership:** Users retain the absolute right to correct, export, expunge, or set retention timers on any memory node.
- **Zero Real Data in Source:** Real personal health data, medical records, and credentials are strictly barred from source control.

---

## 9. What is Implemented in this Repository Today

> [!IMPORTANT]
> This repository contains a **lightweight, runnable FastAPI starter service** implementing the foundational LifeGraph schema, firewall triage logic, and audit trail. It is an engineering sandbox, not the finished multi-platform product.

### ✅ Implemented
- [x] FastAPI REST API service with interactive OpenAPI docs (`/docs`).
- [x] Persistent SQLite database layer (`knowme.db`).
- [x] Memory management: create, inspect, and filter memories with timestamps, confidence scores, and domain tags.
- [x] Policy engine: define and check granular `Allow`, `Ask`, and `Deny` permissions.
- [x] Gated action workflow: reminder requests automatically hold for approval under default policy.
- [x] Audit ledger: interactive approval/rejection endpoints with immutable Action Receipts.

### ⏳ Not Yet Implemented (Planned)
- [ ] Flutter mobile client and accessible UI.
- [ ] ElevenLabs real-time STT / TTS pipelines.
- [ ] AWS infrastructure automation (ECS, RDS pgvector, S3, KMS).
- [ ] Android Health Connect & Google Calendar connectors.
- [ ] ESP32-S3 BLE firmware and pairing protocols.
- [ ] Production authentication, tenant isolation, and encryption-at-rest.

---

## 10. Run the Current Starter Locally

### Prerequisites
* **Python 3.10+** installed
* Git

### Installation & Startup

#### Windows (PowerShell)
```powershell
# 1. Clone repository & navigate to directory
git clone https://github.com/PRIYESHRAJ17/KNOWME.git
cd KNOWME

# 2. Create virtual environment
python -m venv .venv

# 3. Copy configuration
Copy-Item .env.example .env

# 4. Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 5. Start API server
.\.venv\Scripts\python.exe -m uvicorn app:app --reload

macOS / Linux
# 1. Clone repository & navigate to directory
git clone https://github.com/PRIYESHRAJ17/KNOWME.git
cd KNOWME

# 2. Create virtual environment
python3 -m venv .venv

# 3. Copy configuration
cp .env.example .env

# 4. Install dependencies
.venv/bin/python -m pip install -r requirements.txt

# 5. Start API server
.venv/bin/python -m uvicorn app:app --reload

Accessing the API

Once running, explore the service in your browser:

Interactive OpenAPI Docs: http://127.0.0.1:8000/docs
Service Health Check: http://127.0.0.1:8000/health

Step-by-Step API Demo Flow

Run through the core LifeGraph verification loop directly via Swagger UI or curl:

POST /memories — Record a synthetic memory:
json
{
  "content": "Physiotherapy exercises moved to 6:00 PM daily",
  "domain": "health",
  "source": "Dr. Rao consultation note",
  "confidence": 0.95
}
GET /memories — Verify the memory was stored with its generated ID and timestamp.
GET /permissions — Inspect active policy rules (e.g., reminders default to ask).
POST /actions/reminders — Request a reminder based on the new routine:
json
{
  "title": "Evening Physiotherapy",
  "scheduled_time": "18:00",
  "context_memory_id": 1
}
The system halts the operation with status PENDING_APPROVAL.
POST /actions/{action_id}/approval — Grant permission:
json
{
  "decision": "approved"
}
GET /actions — Review the resulting verifiable Action Receipt.
11. Repository Structure
text
KNOWME/
├── docs/
│   └── architecture.md       # Detailed technical design specifications
├── .env.example              # Environment variable template
├── .gitignore                # Git exclusion rules
├── app.py                    # FastAPI application, database schema & endpoints
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
└── requirements.txt          # Python package dependencies
12. Development Principles

To maintain strict engineering rigor, contributors must observe the following:

Explicit Status Tagging: All features must be explicitly categorized as [Planned], [In Progress], [Implemented], or [Tested]. Never document an integration as active without live automated integration tests.
Integration Auditing: Before adding an external service, document:
What data is transmitted and the explicit rationale.
Which user permission rule governs the transaction.
Where credentials, session tokens, and data payloads reside.
Failure handling, timeout limits, and idempotency guarantees.
User controls to inspect, purge, or revoke the integration.
Zero Secret Leakage: Never commit .env, private keys, AWS access secrets, personal medical data, or generated SQLite binaries (knowme.db).


License
This project is licensed under the MIT License. See the LICENSE file for details.
