import numpy as np

from sat_heuristic_validator.dataset import only_3_cnf_dataset
from sat_heuristic_validator.satisfy import count_vars
from sat_heuristic_validator.struct import And, Neg
from sat_heuristic_validator.validation import validate, ValidationMode


def count_signs(f: And) -> bool:
    n = count_vars(f)
    counter = np.zeros(n)
    for or_ in f.xs:
        for term_ in or_.xs:
            if isinstance(term_, Neg):
                counter[term_.x.i - 1] -= 1
            else:
                counter[term_.i - 1] += 1
    mask = 0
    for i in range(n):
        if counter[i] >= 0:
            mask |= 1 << i
    return f.eval(mask=mask)


print(
    validate(
        algorithm=count_signs,
        dataset=only_3_cnf_dataset(n=3),
        validation_mode=ValidationMode.ALL_SAMPLES,
    )
)

# Counterexample: (x1 ∨ x2 ∨ x3)∧(¬x1 ∨ ¬x2 ∨ ¬x3)
