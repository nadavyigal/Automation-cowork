from __future__ import annotations

from email.utils import parseaddr


def is_valid_email(value: str) -> bool:
    if not value:
        return False
    return "@" in parseaddr(value)[1]