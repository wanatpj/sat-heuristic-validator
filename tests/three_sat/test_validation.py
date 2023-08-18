import numpy as np
import pytest

from three_sat.aggregate import PerformanceMetrics
from three_sat.dataset import only_3_cnf_dataset
from three_sat.satisfy import is_satisfiable_brute
from three_sat.validation import validate, ValidationMode


@pytest.mark.parametrize(
    "validation_mode,expected_result",
    [
        (
            ValidationMode.CONFUSION_MATRIX,
            PerformanceMetrics(
                accuracy=1.0,
                precision=np.array([1., 1.]),
                recall=np.array([1., 1.]),
                confusion_matrix=np.array([[1, 0],[0, 255]]),
            ),
        ),
        (ValidationMode.SAMPLE, None)
    ],
)
def test_validate(validation_mode, expected_result):
    assert validate(
        algorithm=is_satisfiable_brute,
        dataset=only_3_cnf_dataset(n=3),
        validation_mode=validation_mode,
    ) == expected_result