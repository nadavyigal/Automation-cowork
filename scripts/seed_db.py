from __future__ import annotations

from src.core.database import init_db, get_session
from src.core.models import LeadEnrichmentJob, RunStatus


def main() -> None:
    init_db()
    with get_session() as session:
        job = LeadEnrichmentJob(
            email="seed@example.com",
            name="Seed User",
            company="Seed Co",
            status=RunStatus.pending,
            payload={"email": "seed@example.com", "name": "Seed User"},
        )
        session.add(job)
    print("Seed data inserted")


if __name__ == "__main__":
    main()