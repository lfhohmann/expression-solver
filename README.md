# Expression Solver

## An expression validator and solver for games like [Mathler](https://www.mathler.com/) and [Nerdle](https://nerdlegame.com/)

### Solver Rules

+ Operations are always performed in **PEDMAS** order
+ Divisions must always result in an integer

### Note

The `ExpressionSolver()` object expects a *config* `dictionary`, containing the following keys:

+ `allow_consecutive_sum_and_sub_operators`: `True` or `False`
+ `allow_leading_zeros`: `True` or `False`
