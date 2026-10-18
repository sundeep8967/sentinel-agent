"""
Core metrics calculation engine for billing & transaction processing.
[AUTO-HEALED BY SENTINEL AGENT]
"""
from typing import List, Dict, Any, Optional

def calculate_discounted_tier(total_amount: Optional[float], tier: Optional[str] = "bronze") -> float:
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

def process_batch_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processes transaction batches, applies tier discounts, and calculates aggregate metrics.
    Robust against None amounts, missing keys, and empty transaction batches.
    """
    total_volume = 0.0
    successful_count = 0
    failed_items = []

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
