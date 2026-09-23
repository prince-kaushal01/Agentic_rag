"""
Simulated email tools — drafts real emails using Gemini; simulates sending.
No SMTP required.
"""
from __future__ import annotations

import asyncio
import logging
import os
import uuid
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client: genai.Client | None = None
_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

_EMAIL_DRAFT_SYSTEM = """\
You are a professional business email writer for NovaTech, an enterprise AI software company.
Write clear, concise, professional emails. Use proper greeting and signature.
Sign emails as "NovaTech Customer Success Team".
Output ONLY the email body (from greeting to signature). Do not add any metadata.
"""


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def _draft_sync(to: str, subject: str, context: str) -> str:
    """Synchronous Gemini call to draft an email."""
    prompt = (
        f"Write a professional email to: {to}\n"
        f"Subject: {subject}\n"
        f"Context / key points to cover:\n{context}\n\n"
        f"Write the complete email body now:"
    )
    client = _get_client()
    resp = client.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=_EMAIL_DRAFT_SYSTEM,
            max_output_tokens=512,
            temperature=0.3,
        ),
    )
    return (resp.text or "").strip()


async def draft_email(
    to: str,
    subject: str,
    context: str = "",
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """
    Use Gemini to draft a professional email.
    Returns the draft for review; does NOT send.
    """
    if not to:
        return {"error": "Recipient email address is required."}
    if not subject:
        return {"error": "Email subject is required."}

    draft_body = await asyncio.to_thread(_draft_sync, to, subject, context)

    return {
        "draft_id": f"DRAFT-{uuid.uuid4().hex[:8].upper()}",
        "to": to,
        "subject": subject,
        "body": draft_body,
        "status": "draft",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "note": "This is a draft. Call send_email to dispatch it.",
    }


async def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str | None = None,
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """
    Simulate sending an email (no real SMTP — logs the action).
    In production, wire this to SendGrid / SES / Outlook.
    """
    if not to or not subject or not body:
        return {"error": "to, subject, and body are all required."}

    message_id = f"MSG-{uuid.uuid4().hex[:12].upper()}"
    sent_at = datetime.now(timezone.utc).isoformat()

    # Log the simulated send (in production, call your email provider here)
    logger.info(
        "[SIMULATED EMAIL SEND] id=%s to=%s cc=%s subject=%r at=%s",
        message_id, to, cc or "none", subject, sent_at,
    )

    return {
        "status": "sent",
        "message_id": message_id,
        "to": to,
        "cc": cc,
        "subject": subject,
        "sent_at": sent_at,
        "note": "Email delivery is simulated. No actual message was dispatched.",
    }
