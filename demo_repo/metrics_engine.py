"""
Core metrics calculation engine for billing & transaction processing.
[AUTO-HEALED BY SENTINEL AGENT]
"""
from bisect import bisect_left, insort
from collections import deque
from numbers import Real
from typing import Iterable, List, Optional, TypedDict


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


def calculate_rolling_percentile(
    values: Iterable[float], window_size: int, percentile: Real
) -> List[float]:
    """Calculate a percentile for each complete rolling window.

    The active window is kept in a fixed-size :class:`collections.deque`,
    while a sorted list makes percentile lookup constant time.  ``bisect`` is
    used to insert each incoming value and to locate the outgoing value when
    the window advances, avoiding a full sort for every window.

    Only complete windows are returned.  For example, a five-value input with
    a window size of three produces three percentile values.  Percentiles use
    the usual linear interpolation between the two surrounding ranks, with
    ``0`` selecting the minimum and ``100`` selecting the maximum.

    Args:
        values: Numeric values in arrival order.  Any iterable is accepted,
            including a generator.
        window_size: Number of values in each fixed rolling window. Must be
            a positive integer.
        percentile: Requested percentile on the inclusive ``0`` to ``100``
            scale.

    Returns:
        One interpolated percentile for every complete rolling window.

    Raises:
        ValueError: If ``window_size`` is not positive or ``percentile`` is
            outside the inclusive ``0`` to ``100`` range.
    """
    if isinstance(window_size, bool) or not isinstance(window_size, int) or window_size < 1:
        raise ValueError("window_size must be a positive integer")
    if isinstance(percentile, bool) or not isinstance(percentile, Real) or not 0 <= percentile <= 100:
        raise ValueError("percentile must be between 0 and 100")

    window: deque[float] = deque(maxlen=window_size)
    sorted_window: List[float] = []
    result: List[float] = []

    for value in values:
        if len(window) == window_size:
            outgoing = window[0]
            del sorted_window[bisect_left(sorted_window, outgoing)]
            window.popleft()

        window.append(value)
        insort(sorted_window, value)

        if len(window) == window_size:
            rank = (len(sorted_window) - 1) * float(percentile) / 100.0
            lower_index = int(rank)
            upper_index = min(lower_index + 1, len(sorted_window) - 1)
            weight = rank - lower_index
            lower = sorted_window[lower_index]
            upper = sorted_window[upper_index]
            result.append(float(lower + (upper - lower) * weight))

    return result


# Keep the concise name available for callers that treat this as a rolling
# statistic rather than a general metrics calculation.
rolling_percentile = calculate_rolling_percentile


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
