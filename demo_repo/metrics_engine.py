"""
Core metrics calculation engine for billing & transaction processing.
[AUTO-HEALED BY SENTINEL AGENT]
"""
from typing import List, Optional, TypedDict


class Transaction(TypedDict, total=False):
    """Transaction fields consumed by the batch metrics engine."""

    id: str
    amount: Optional[float]
    tier: Optional[str]


class FailedTransaction(TypedDict):
    """Details recorded when a transaction cannot be processed."""

    item: Transaction
    reason: str


class BatchMetrics(TypedDict):
    """Aggregate metrics returned for a processed transaction batch."""

    total_volume: float
    successful_count: int
    average_ticket: float
    failed_items: List[FailedTransaction]


def calculate_discounted_tier(
    total_amount: Optional[float], tier: Optional[str] = "bronze"
) -> float:
    """Apply the discount for ``tier`` and return the resulting amount.

    ``None`` amounts are treated as zero so callers can safely use this
    helper while validating partially populated transaction records. Unknown
    tiers receive no discount, and a missing tier defaults to bronze.

    Args:
        total_amount: Pre-discount transaction amount, or ``None`` when the
            amount is unavailable.
        tier: Customer tier used to select the discount rate.

    Returns:
        The discounted amount, or ``0.0`` when ``total_amount`` is ``None``.
    """
    if total_amount is None:
        return 0.0
    discount_rates = {
        "bronze": 0.05,
        "silver": 0.10,
        "gold": 0.20
    }
    tier_clean = (tier or "bronze").lower()
    rate = discount_rates.get(tier_clean, 0.0)
    return total_amount * (1.0 - rate)

def process_batch_transactions(transactions: List[Transaction]) -> BatchMetrics:
    """Process transactions and calculate discounted aggregate metrics.

    Each transaction with a numeric amount contributes its discounted value to
    the batch totals. Records with a missing or ``None`` amount are retained
    in ``failed_items`` instead of interrupting the rest of the batch.

    Args:
        transactions: Transaction records to process. The list may be empty.

    Returns:
        A :class:`BatchMetrics` mapping containing the rounded total volume,
        successful transaction count, average ticket, and failed records.
    """
    total_volume = 0.0
    successful_count = 0
    failed_items: List[FailedTransaction] = []

    for tx in transactions:
        amt = tx.get("amount")
        tier = tx.get("tier", "bronze")
        
        if amt is None:
            failed_items.append({"item": tx, "reason": "Missing or null amount"})
            continue

        final_price = calculate_discounted_tier(amt, tier)
        total_volume += final_price
        successful_count += 1

    average_ticket = (total_volume / successful_count) if successful_count > 0 else 0.0

    return {
        "total_volume": round(total_volume, 2),
        "successful_count": successful_count,
        "average_ticket": round(average_ticket, 2),
        "failed_items": failed_items
    }
