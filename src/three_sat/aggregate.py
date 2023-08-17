from abc import abstractmethod

import sklearn.metrics

from three_sat.struct import And


class AggregationError(Exception):
    pass


class Aggregator:

    @abstractmethod
    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        pass

    @abstractmethod
    def done(self):
        pass


class ConfusionAggregator(Aggregator):

    def __init__(self):
        self.y_true = []
        self.y_pred = []

    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        self.y_true.append(y_expected)
        self.y_pred.append(y_actual)

    def done(self):
        print(sklearn.metrics.confusion_matrix(y_true=self.y_true, y_pred=self.y_pred))


class SampleAggregator(Aggregator):

    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        if y_actual != y_expected:
            raise AggregationError(f"{y_actual=} {x=} {y_expected=}")

    def done(self):
        pass
