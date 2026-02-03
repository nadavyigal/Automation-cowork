from src.automations.lead_enrichment.webhook import LeadInput


def test_lead_input_validation():
    lead = LeadInput(email="test@example.com", name="Test", company="Acme")
    assert lead.email == "test@example.com"