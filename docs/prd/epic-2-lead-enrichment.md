# Epic 2: Lead Enrichment

## Scope
- Webhook receiver
- Multi-provider enrichment with fallback
- Caching and persistence
- Email notifications

## Acceptance Criteria
- Webhook returns 202
- Enrichment tries providers in order
- Results stored with status
- Notification sent on success/failure