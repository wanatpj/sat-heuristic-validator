import pytest

from sat_heuristic_validator.struct import And, Neg, Or, Var


@pytest.mark.parametrize(
    "formula,string,representation",
    [
        (
            And(
                Or(Var(i=1), Var(i=2), Neg(Var(i=3))),
                Or(Var(i=1), Var(i=4), Neg(Var(i=5))),
            ),
            "(x1 ∨ x2 ∨ ¬x3)∧(x1 ∨ x4 ∨ ¬x5)",
            "And(Or(Var(1), Var(2), Neg(Var(3))), Or(Var(1), Var(4), Neg(Var(5))))",
        ),
        (
            Or(Var(i=1), Var(i=2), Neg(Var(i=3))),
            "x1 ∨ x2 ∨ ¬x3",
            "Or(Var(1), Var(2), Neg(Var(3)))",
        ),
        (
            Var(i=1),
            "x1",
            "Var(1)",
        ),
        (
            Neg(Var(i=2)),
            "¬x2",
            "Neg(Var(2))",
        ),
    ],
)
def test_struct(formula, string, representation):
    assert str(formula) == string
    assert repr(formula) == representation


@pytest.mark.parametrize(
    "formula,mask,expectation",
    [
        (Var(i=2), 0b0001, False),
        (Var(i=2), 0b0010, True),
        (Var(i=2), 0b0100, False),
        (Var(i=2), 0b1000, False),
        (Neg(Var(i=3)), 0b0001, True),
        (Neg(Var(i=3)), 0b0010, True),
        (Neg(Var(i=3)), 0b0100, False),
        (Neg(Var(i=3)), 0b1000, True),
        (Or(Var(i=1), Neg(Var(i=3))), 0b0001, True),
        (Or(Var(i=1), Neg(Var(i=3))), 0b0010, True),
        (Or(Var(i=1), Neg(Var(i=3))), 0b0100, False),
        (Or(Var(i=1), Neg(Var(i=3))), 0b1000, True),
        (Or(Var(i=1), Neg(Var(i=3))), 0b0101, True),
        (Or(Var(i=1), Neg(Var(i=3))), 0b0110, False),
        (Or(Var(i=1), Neg(Var(i=3))), 0b1100, False),
        (Or(), 0, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b000, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b001, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b010, True),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b011, True),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b100, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b101, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b110, False),
        (And(Or(Var(i=2)), Or(Var(i=1), Neg(Var(i=3)))), 0b111, True),
        (And(), 0, True),
    ],
)
def test_eval(formula, mask, expectation):
    assert formula.eval(mask=mask) == expectation
