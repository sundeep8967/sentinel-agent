import pytest
from metrics_engine import process_batch_transactions, calculate_discounted_tier

def test_happy_path_batch():
    batch = [
        {"id": "tx_1", "amount": 100.0, "tier": "gold"},
        {"id": "tx_2", "amount": 50.0, "tier": "silver"},
    ]
    result = process_batch_transactions(batch)
    assert result["successful_count"] == 2
    assert result["total_volume"] == 125.0  # 80 + 45
    assert result["average_ticket"] == 62.5

def test_empty_batch_handling():
    # Should not raise ZeroDivisionError
    result = process_batch_transactions([])
    assert result["successful_count"] == 0
    assert result["total_volume"] == 0.0
    assert result["average_ticket"] == 0.0

def test_missing_or_none_amount_resilience():
    batch = [
        {"id": "tx_valid", "amount": 100.0, "tier": "bronze"},
        {"id": "tx_corrupt", "amount": None, "tier": "silver"},
        {"id": "tx_missing_key", "tier": "gold"},
    ]
    result = process_batch_transactions(batch)
    assert result["successful_count"] == 1
    assert result["total_volume"] == 95.0
    assert len(result["failed_items"]) == 2
