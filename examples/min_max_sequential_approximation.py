import numpy as np
import torch

from sat_heuristic_validator.dataset import only_3_cnf_dataset
from sat_heuristic_validator.satisfy import count_vars
from sat_heuristic_validator.struct import And, Neg
from sat_heuristic_validator.validation import validate, ValidationMode


def average_tensor(x: torch.Tensor, n: int) -> torch.Tensor:
    if n == 0:
        return x.prod() ** (1 / x.numel())
    return ((x ** n).sum() / x.numel()) ** (1 / n)


def compile_formula(f: And, x: torch.Tensor, min_deg: int, max_deg: int) -> torch.Tensor:
    neg_x = 1 - x
    or_tensors = []
    for or_ in f.xs:
        or_input_tensor = torch.cat([
            neg_x[term_.x.i - 1].reshape(1) if isinstance(term_, Neg) else x[term_.i - 1].reshape(1)
            for term_ in or_.xs
        ])
        or_tensors.append(average_tensor(or_input_tensor, max_deg).reshape(1))
    return average_tensor(torch.cat(or_tensors), min_deg)


def min_max_sequential_approximation(f: And) -> bool:
    n = count_vars(f)
    if n == 0:
        return True
    x = torch.tensor(np.random.rand(n), requires_grad=True)
    for i in range(n):
        fn = compile_formula(f, x=x, min_deg=1-i, max_deg=1+i)
        fn.backward()
        with torch.no_grad():
            x += x.grad
    return (compile_formula(f, x=(x >= 0.5).float(), min_deg=1-n, max_deg=1+n) > 0.5).item()


print(validate(
    algorithm=min_max_sequential_approximation,
    dataset=only_3_cnf_dataset(n=3),
    validation_mode=ValidationMode.ALL_SAMPLES,
))