"""Integration coverage for end-to-end batch metrics processing."""

import pytest

from metrics_engine import process_batch_transactions


@pytest.mark.parametrize(
    ("transactions", "expected"),
    [
        pytest.param(
            [],
            {
                "total_volume": 0.0,
                "successful_count": 0,
                "average_ticket": 0.0,
                "failed_items": [],
            },
            id="empty-workload",
        ),
        pytest.param(
            [
                {"id": "gold", "amount": 100.0, "tier": "gold"},
                {"id": "silver", "amount": 200.0, "tier": "silver"},
                {"id": "bronze", "amount": 50.0, "tier": "bronze"},
                {"id": "default", "amount": 20.0},
                {"id": "case-insensitive", "amount": 25.0, "tier": "GOLD"},
                {"id": "unknown-tier", "amount": 15.0, "tier": "platinum"},
            ],
            {
                "total_volume": 361.5,
                "successful_count": 6,
                "average_ticket": 60.25,
                "failed_items": [],
            },
            id="mixed-discount-tiers",
        ),
        pytest.param(
            [
                {"id": "valid-bronze", "amount": 100.0, "tier": "bronze"},
                {"id": "null-amount", "amount": None, "tier": "silver"},
                {"id": "missing-amount", "tier": "gold"},
                {"id": "valid-gold", "amount": 80.0, "tier": "gold"},
                {"id": "valid-default", "amount": 20.0},
            ],
            {
                "total_volume": 178.0,
                "successful_count": 3,
                "average_ticket": 59.33,
                "failed_items": [
                    {
                        "item": {
                            "id": "null-amount",
                            "amount": None,
                            "tier": "silver",
                        },
                        "reason": "Missing or null amount",
                    },
                    {
                        "item": {"id": "missing-amount", "tier": "gold"},
                        "reason": "Missing or null amount",
                    },
                ],
            },
            id="partial-invalid-workload",
        ),
        pytest.param(
            [
                {
                    "id": f"large-{index}",
                    "amount": 10.0,
                    "tier": "gold" if index % 2 == 0 else "silver",
                }
                for index in range(1000)
            ],
            {
                "total_volume": 8500.0,
                "successful_count": 1000,
                "average_ticket": 8.5,
                "failed_items": [],
            },
            id="large-balanced-workload",
        ),
    ],
)
def test_batch_processing_across_workload_conditions(transactions, expected):
    """Process empty, mixed, invalid, and large batches end to end."""
    assert process_batch_transactions(transactions) == expected
