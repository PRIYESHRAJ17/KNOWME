"""KNOWME starter MVP: evidence-linked memories, permission checks and action receipts.

This is a local demonstration framework. It stores data in SQLite and simulates
creating a reminder; it does not send notifications, access medical records,
call ElevenLabs, or deploy to AWS yet.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_NAME = "KNOWME MVP"
DB_PATH = Path(os.getenv("KNOWME_DB_PATH", "knowme.db"))

app = FastAPI(
    title=APP_NAME,
    description=(
        "A small local prototype of KNOWME's core loop: save an evidence-linked "
        "memory, check a user-defined permission, require approval, and record an action receipt."
    ),
    version="0.1.0",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialise_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with db_connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                domain TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT
            );
            CREATE TABLE IF NOT EXISTS permissions (
                action_type TEXT PRIMARY KEY,
                decision TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS actions (
                id TEXT PRIMARY KEY,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                scheduled_for TEXT NOT NULL,
                memory_id TEXT,
                status TEXT NOT NULL,
                approved_at TEXT,
                created_at TEXT NOT NULL,
                receipt TEXT
            );
            """
        )
        # Default policy: ask before creating reminders or sharing information.
        db.execute(
            "INSERT OR IGNORE INTO permissions(action_type, decision, updated_at) VALUES (?, ?, ?)",
            ("create_reminder", "ask", now_iso()),
        )
        db.execute(
            "INSERT OR IGNORE INTO permissions(action_type, decision, updated_at) VALUES (?, ?, ?)",
            ("notify_family", "ask", now_iso()),
        )


@app.on_event("startup")
def on_startup() -> None:
    initialise_db()


class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=2, max_length=1000)
    domain: str = Field(default="personal", max_length=50)
    source: str = Field(..., min_length=2, max_length=300)
    confidence: Literal["user_confirmed", "source_recorded", "inferred"] = "user_confirmed"
    expires_at: str | None = Field(default=None, description="Optional ISO-8601 expiry chosen by the user")


class PermissionUpdate(BaseModel):
    decision: Literal["allow", "ask", "deny"]


class ReminderCreate(BaseModel):
    description: str = Field(..., min_length=2, max_length=300)
    scheduled_for: str = Field(..., description="Example: 09:00 AM (display text for this demo)")
    memory_id: str | None = None


class ApprovalRequest(BaseModel):
    approved: bool


@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME, "mode": "local-demo"}


@app.post("/memories", status_code=201)
def create_memory(payload: MemoryCreate):
    memory_id = str(uuid4())
    created_at = now_iso()
    with db_connection() as db:
        db.execute(
            """INSERT INTO memories(id, content, domain, source, confidence, created_at, expires_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                memory_id,
                payload.content,
                payload.domain,
                payload.source,
                payload.confidence,
                created_at,
                payload.expires_at,
            ),
        )
    return {
        "id": memory_id,
        "content": payload.content,
        "domain": payload.domain,
        "source": payload.source,
        "confidence": payload.confidence,
        "created_at": created_at,
        "expires_at": payload.expires_at,
        "status": "stored",
    }


@app.get("/memories")
def list_memories():
    with db_connection() as db:
        rows = db.execute("SELECT * FROM memories ORDER BY created_at DESC").fetchall()
    return {"items": [dict(row) for row in rows], "count": len(rows)}


@app.get("/permissions")
def list_permissions():
    with db_connection() as db:
        rows = db.execute("SELECT * FROM permissions ORDER BY action_type").fetchall()
    return {"items": [dict(row) for row in rows]}


@app.put("/permissions/{action_type}")
def update_permission(action_type: str, payload: PermissionUpdate):
    with db_connection() as db:
        db.execute(
            """INSERT INTO permissions(action_type, decision, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(action_type) DO UPDATE SET decision=excluded.decision,
               updated_at=excluded.updated_at""",
            (action_type, payload.decision, now_iso()),
        )
    return {"action_type": action_type, "decision": payload.decision, "updated_at": now_iso()}


@app.post("/actions/reminders", status_code=201)
def request_reminder(payload: ReminderCreate):
    with db_connection() as db:
        if payload.memory_id:
            memory = db.execute("SELECT id FROM memories WHERE id = ?", (payload.memory_id,)).fetchone()
            if memory is None:
                raise HTTPException(status_code=404, detail="Linked memory was not found")
        permission = db.execute(
            "SELECT decision FROM permissions WHERE action_type = ?", ("create_reminder",)
        ).fetchone()
        decision = permission["decision"] if permission else "ask"

        action_id = str(uuid4())
        created_at = now_iso()
        status = "pending_approval" if decision == "ask" else ("approved" if decision == "allow" else "denied")
        approved_at = created_at if decision == "allow" else None
        receipt = None
        if status == "approved":
            receipt = f"DEMO-RECEIPT | {action_id} | approved by saved policy | {created_at}"
        db.execute(
            """INSERT INTO actions(id, action_type, description, scheduled_for, memory_id,
               status, approved_at, created_at, receipt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                action_id,
                "create_reminder",
                payload.description,
                payload.scheduled_for,
                payload.memory_id,
                status,
                approved_at,
                created_at,
                receipt,
            ),
        )
    return {
        "action_id": action_id,
        "action": "create_reminder",
        "description": payload.description,
        "scheduled_for": payload.scheduled_for,
        "permission_decision": decision,
        "status": status,
        "approval_required": status == "pending_approval",
        "note": "Demo only: this records a reminder request; it does not create a phone notification.",
        "receipt": receipt,
    }


@app.post("/actions/{action_id}/approval")
def approve_action(action_id: str, payload: ApprovalRequest):
    with db_connection() as db:
        action = db.execute("SELECT * FROM actions WHERE id = ?", (action_id,)).fetchone()
        if action is None:
            raise HTTPException(status_code=404, detail="Action was not found")
        if action["status"] != "pending_approval":
            raise HTTPException(status_code=409, detail=f"Action is already {action['status']}")

        decided_at = now_iso()
        if payload.approved:
            receipt = (
                f"KNOWME DEMO ACTION RECEIPT\n"
                f"Action ID: {action_id}\n"
                f"Action: {action['description']}\n"
                f"Scheduled for: {action['scheduled_for']}\n"
                f"User approval: YES\n"
                f"Source memory: {action['memory_id'] or 'not linked'}\n"
                f"Approved at: {decided_at}\n"
                f"Outcome: Recorded in local demo database; no external notification sent."
            )
            status = "approved_demo_only"
            approved_at = decided_at
        else:
            receipt = f"KNOWME DEMO ACTION RECEIPT | {action_id} | denied by user | {decided_at}"
            status = "denied"
            approved_at = None

        db.execute(
            "UPDATE actions SET status=?, approved_at=?, receipt=? WHERE id=?",
            (status, approved_at, receipt, action_id),
        )
    return {"action_id": action_id, "status": status, "receipt": receipt}


@app.get("/actions")
def list_actions():
    with db_connection() as db:
        rows = db.execute("SELECT * FROM actions ORDER BY created_at DESC").fetchall()
    return {"items": [dict(row) for row in rows], "count": len(rows)}
