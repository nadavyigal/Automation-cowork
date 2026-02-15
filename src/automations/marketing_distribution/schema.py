from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SocialPostDraft:
    post_id: str
    publish_date: date
    locale: str
    platform: str
    account_target: str
    post_copy: str
    utm_url: str
    status: str

    @property
    def normalized_platform(self) -> str:
        value = self.platform.strip().lower()
        aliases = {
            "twitter": "x",
            "x/twitter": "x",
            "linkedin.com": "linkedin",
            "fb": "community",
            "facebook": "community",
            "telegram": "community",
            "whatsapp": "community",
        }
        return aliases.get(value, value)

    @property
    def rendered_content(self) -> str:
        if self.utm_url in self.post_copy:
            return self.post_copy
        return f"{self.post_copy}\n\n{self.utm_url}"
