import numpy as np
import pytest

from sat_heuristic_validator.aggregate import PerformanceMetrics
from sat_heuristic_validator.dataset import only_3_cnf_dataset
from sat_heuristic_validator.satisfy import is_satisfiable_brute
from sat_heuristic_validator.validation import validate, ValidationMode


@pytest.mark.parametrize(
    "validation_mode,expected_result",
    [
        (
            ValidationMode.CONFUSION_MATRIX,
            PerformanceMetrics(
                accuracy=1.0,
                precision=np.array([1.0, 1.0]),
                recall=np.array([1.0, 1.0]),
                confusion_matrix=np.array([[1, 0], [0, 255]]),
            ),
        ),
        (ValidationMode.SAMPLE, None),
    ],
)
def test_validate(validation_mode, expected_result):
    assert (
        validate(
            algorithm=is_satisfiable_brute,
            dataset=only_3_cnf_dataset(n=3),
            validation_mode=validation_mode,
        )
        == expected_result
    )
