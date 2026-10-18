"""Benchmark rolling percentile throughput on a reproducible metric stream."""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path
from statistics import median


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from demo_repo.metrics_engine import calculate_rolling_percentile


SAMPLE_COUNT = 10_000
WINDOW_SIZE = 60
PERCENTILE = 95
REPEAT_COUNT = 5
SYNTHETIC_SEED = 20261018


def build_samples() -> list[float]:
    """Return a deterministic stream of synthetic latency metrics."""
    generator = random.Random(SYNTHETIC_SEED)
    return [generator.gauss(mu=100.0, sigma=15.0) for _ in range(SAMPLE_COUNT)]


def main() -> None:
    """Run the benchmark and print the median throughput across repetitions."""
    samples = build_samples()
    durations: list[float] = []
    result: list[float] = []

    for _ in range(REPEAT_COUNT):
        started_at = time.perf_counter()
        result = calculate_rolling_percentile(
            samples, window_size=WINDOW_SIZE, percentile=PERCENTILE
        )
        durations.append(time.perf_counter() - started_at)

    expected_windows = SAMPLE_COUNT - WINDOW_SIZE + 1
    if len(result) != expected_windows:
        raise RuntimeError(
            f"expected {expected_windows} complete windows, got {len(result)}"
        )

    elapsed = median(durations)
    throughput = SAMPLE_COUNT / elapsed

    print("Rolling percentile benchmark")
    print(f"Samples: {SAMPLE_COUNT:,}")
    print(f"Window: {WINDOW_SIZE} | Percentile: p{PERCENTILE}")
    print(f"Complete windows: {len(result):,}")
    print(f"Median elapsed time ({REPEAT_COUNT} runs): {elapsed:.6f} seconds")
    print(f"Throughput: {throughput:,.0f} samples/second")


if __name__ == "__main__":
    main()
