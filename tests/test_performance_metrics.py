"""Unit tests for the fixed-window rolling percentile calculation."""

import math
import sys
from pathlib import Path

import pytest

# The demo service is a source tree rather than an installed package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from demo_repo.metrics_engine import calculate_rolling_percentile


def test_returns_one_median_for_each_complete_window():
    values = [9, 1, 5, 3, 7]

    result = calculate_rolling_percentile(values, window_size=3, percentile=50)

    assert result == [5.0, 3.0, 5.0]


def test_interpolates_between_ranks_and_supports_percentile_boundaries():
    values = [0, 10, 20, 30]

    assert calculate_rolling_percentile(values, window_size=3, percentile=25) == [
        5.0,
        15.0,
    ]
    assert calculate_rolling_percentile(values, window_size=3, percentile=0) == [
        0.0,
        10.0,
    ]
    assert calculate_rolling_percentile(values, window_size=3, percentile=100) == [
        20.0,
        30.0,
    ]


def test_sliding_window_removes_the_oldest_duplicate_correctly():
    values = [1, 2, 2, 100, 3]

    result = calculate_rolling_percentile(values, window_size=3, percentile=50)

    assert result == [2.0, 2.0, 3.0]


def test_accepts_generators_and_omits_incomplete_windows():
    values = (value for value in [4, 8])

    assert calculate_rolling_percentile(values, window_size=3, percentile=50) == []


@pytest.mark.parametrize("window_size", [0, -1, 1.5, True])
def test_rejects_invalid_window_sizes(window_size):
    with pytest.raises(ValueError, match="window_size"):
        calculate_rolling_percentile([1, 2, 3], window_size, 50)


@pytest.mark.parametrize("percentile", [-0.1, 100.1, math.nan, True])
def test_rejects_percentiles_outside_the_supported_range(percentile):
    with pytest.raises(ValueError, match="percentile"):
        calculate_rolling_percentile([1, 2, 3], 2, percentile)
