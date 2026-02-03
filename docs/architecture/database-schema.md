# Database Schema

Tables:
- automation_runs
- lead_enrichment_jobs
- pipeline_executions
- social_media_posts
- api_usage

Relationships:
- automation_runs -> lead_enrichment_jobs (1:N)
- automation_runs -> pipeline_executions (1:N)
- automation_runs -> social_media_posts (1:N)