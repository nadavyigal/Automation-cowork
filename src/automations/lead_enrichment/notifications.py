from __future__ import annotations

import smtplib
from email.message import EmailMessage
from loguru import logger

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.core.config import settings


def send_email(subject: str, body: str, to_address: str) -> None:
    if settings.sendgrid_api_key:
        _send_sendgrid(subject, body, to_address)
        return

    if settings.smtp_host and settings.smtp_username and settings.smtp_password:
        _send_smtp(subject, body, to_address)
        return

    logger.warning("No email provider configured; skipping notification")


def send_lead_notification(
    *,
    job_id: int,
    email: str,
    provider: str | None,
    status: str,
    error_message: str | None = None,
) -> None:
    if not settings.notify_email:
        return

    if status == "completed" and not settings.notify_on_success:
        return

    if status == "failed" and not settings.notify_on_failure:
        return

    subject = f"Lead Enrichment {status.upper()} - {email}"
    body_lines = [
        f"Job ID: {job_id}",
        f"Email: {email}",
        f"Status: {status}",
    ]
    if provider:
        body_lines.append(f"Provider: {provider}")
    if error_message:
        body_lines.append(f"Error: {error_message}")

    body = "\n".join(body_lines)
    send_email(subject, body, settings.notify_email)


def _send_smtp(subject: str, body: str, to_address: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from or settings.smtp_username
    msg["To"] = to_address
    msg.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port or 587) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)

    logger.info("SMTP email sent")


def _send_sendgrid(subject: str, body: str, to_address: str) -> None:
    message = Mail(
        from_email=settings.smtp_from or "notifications@automation-cowork.local",
        to_emails=to_address,
        subject=subject,
        plain_text_content=body,
    )

    client = SendGridAPIClient(settings.sendgrid_api_key)
    client.send(message)
    logger.info("SendGrid email sent")
