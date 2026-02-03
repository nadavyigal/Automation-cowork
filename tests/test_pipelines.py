from src.automations.data_pipelines.transformers import transform_customers


def test_transform_dedupes_by_email():
    rows = [
        {"email": "Test@Example.com", "updated_at": 1},
        {"email": "test@example.com", "updated_at": 2},
        {"email": "other@example.com", "updated_at": 1},
    ]
    result = transform_customers(rows)
    assert len(result) == 2
    emails = {row["email"] for row in result}
    assert "test@example.com" in emails
    assert "other@example.com" in emails