from __future__ import annotations

import argparse

from src.automations.lead_enrichment.webhook import process_lead
from src.automations.lead_enrichment.storage import create_lead_job
from src.automations.data_pipelines.etl_job import run_etl_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Run automation tasks")
    parser.add_argument("--lead", type=str, help="Email address to enrich")
    parser.add_argument("--name", type=str, default=None, help="Lead name")
    parser.add_argument("--company", type=str, default=None, help="Lead company")
    parser.add_argument("--etl", action="store_true", help="Run data pipeline ETL")
    args = parser.parse_args()

    if args.etl:
        run_etl_job()
        return

    if args.lead:
        payload = {"email": args.lead, "name": args.name, "company": args.company}
        job = create_lead_job(payload)
        process_lead(job.id, payload)
        return

    parser.print_help()


if __name__ == "__main__":
    main()