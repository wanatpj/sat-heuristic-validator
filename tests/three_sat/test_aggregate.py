from unittest.mock import ANY

import numpy as np
import pytest

from three_sat.aggregate import AggregationError, ConfusionAggregator, PerformanceMetrics, SampleAggregator


def test_sample_aggregator():
    aggregator = SampleAggregator()

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=True)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)

    with pytest.raises(AggregationError):
        aggregator.aggregate(y_actual=True, x=ANY, y_expected=False)

    with pytest.raises(AggregationError):
        aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)


def test_confusion_aggregator():
    aggregator = ConfusionAggregator()

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=True)

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=False)
    aggregator.aggregate(y_actual=True, x=ANY, y_expected=False)

    aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)

    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)
    assert aggregator.done() == PerformanceMetrics(
        accuracy=5 / 10,
        precision=np.array([4 / 7, 1 / 3]),
        recall=np.array([4 / 6, 1 / 4]),
        confusion_matrix=[[4, 2], [3, 1]],
    )