import pytest

from three_sat.struct import And, Neg, Or, Var
from three_sat.satisfy import is_satisfiable_brute


@pytest.mark.parametrize(
    "formula,expectation",
    [
        (And(), True),
        (And(Or(Var(1))), True),
        (And(Or(Var(1)), Or(Neg(Var(1)))), False),
        (And(Or(Var(1), Var(2)), Or(Neg(Var(1)))), True),
        (And(Or(Var(1), Var(2)), Or(Neg(Var(2)))), True),
        (And(Or(Var(1), Var(2)), Or(Neg(Var(1))), Or(Neg(Var(2)))), False),
    ],
)
def test_is_satisfiable_brute(formula, expectation):
    is_satisfiable_brute(formula) == expectation


# @pytest.mark.parametrize(
#     "three_sat_formula",
#     [
#         *gen_3_sat_formulas(n=3),
#         *gen_3_sat_formulas(n=4),
#         *gen_3_sat_formulas(n=5),
#         *gen_3_sat_formulas(n=6),
#         *gen_3_sat_formulas(n=7),
#         *gen_3_sat_formulas(n=8),
#         *gen_3_sat_formulas(n=9),
#     ]
# )
# def test_is_satisfiable_brute(three_sat_formula):
#     assert solve_3_sat_brute(three_sat_formula) == researched_algorithm(three_sat_formula)
