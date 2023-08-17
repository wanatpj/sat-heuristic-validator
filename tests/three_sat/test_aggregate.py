from unittest.mock import ANY

import pytest

from three_sat.aggregate import AggregationError, ConfusionAggregator, SampleAggregator


def test_sample_aggregator(capsys):
    aggregator = SampleAggregator()

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=True)
    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""

    with pytest.raises(AggregationError):
        aggregator.aggregate(y_actual=True, x=ANY, y_expected=False)

    with pytest.raises(AggregationError):
        aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""


def test_confusion_aggregator(capsys):
    aggregator = ConfusionAggregator()

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=True)
    aggregator.done()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "[[1]]\n"

    aggregator.aggregate(y_actual=True, x=ANY, y_expected=False)
    aggregator.done()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "[[0 1]\n [0 1]]\n"

    aggregator.aggregate(y_actual=False, x=ANY, y_expected=True)
    aggregator.done()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "[[0 1]\n [1 1]]\n"

    aggregator.aggregate(y_actual=False, x=ANY, y_expected=False)
    aggregator.done()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "[[1 1]\n [1 1]]\n"