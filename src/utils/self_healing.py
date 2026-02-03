from __future__ import annotations

from loguru import logger
from openai import OpenAI

from src.core.config import settings


def auto_fix_api_error(error_message: str, failing_code: str) -> str:
    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY is not configured; skipping auto-fix")
        return ""

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = f"""
This Python code is failing with the following error:

ERROR: {error_message}

CODE:
{failing_code}

Suggest a fixed version of the code that handles this error.
Return ONLY the corrected code, no explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    fixed_code = response.choices[0].message.content or ""
    logger.info("Auto-generated fix received")
    return fixed_code