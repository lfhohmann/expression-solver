#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Tests
----------

This module performs unit tests for the expression solver class.
"""

import unittest

from expression_solver import ExpressionSolver


__author__ = "Lucas Hohmann"
__email__ = "lfhohmann@gmail.com"
__user__ = "@lfhohmann"

__status__ = "Production"
__date__ = "2022/03/06"
__version__ = "1.0.0"
__license__ = "MIT"


class TestSolver(unittest.TestCase):
    """
    Solver Test
    -----------------------

    Tests the ExpressionSolver class
    """

    def test_general(self):
        """Tests cases that are 'not configuration dependent'"""

        # Define the configuration parameters
        config = {
            "allow_consecutive_sum_and_sub_operators": True,
            "allow_leading_zeros": True,
        }

        # Instantiate the solver
        solver = ExpressionSolver(config)

        # Define the cases
        valid_cases = [
            ("4-18/+2", [-5], "Valid consecutive operators"),
            ("136+0/7", [136], "Zero divided by any number is zero"),
            ("3--14/7", [5], "Valid consecutive operators"),
            ("3--++12", [15], "Valid consecutive operators"),
        ]

        invalid_cases = [
            ("/7-78/9", [], "invalid starting operator"),
            ("*1-45/2", [], "invalid starting operator"),
            ("7-78/9/", [], "invalid trailing operator"),
            ("1-45/2*", [], "invalid trailing operator"),
            ("4+123/0", [], "No divisions by zero allowed"),
            ("2*13/-0", [], "No divisions by zero allowed"),
            ("4+89*/0", [], "Invalid consecutive operators"),
            ("7-123/2", [], "Divisions must result in an integer"),
        ]

        # Run the tests
        for case in valid_cases:
            self.assertEqual(solver.solve(case[0]), case[1], case[2])

        for case in invalid_cases:
            self.assertEqual(solver.solve(case[0]), case[1], case[2])

    def test_mathler(self):
        """Tests cases configured for the Mathler game"""

        # Define the configuration parameters
        config = {
            "allow_consecutive_sum_and_sub_operators": True,
            "allow_leading_zeros": False,
        }

        # Instantiate the solver
        solver = ExpressionSolver(config)

        # Define the valid cases
        valid_cases = [
            ("4+561*0", [4], "Single zeros are allowed"),
            ("+0-4+10", [6], "Single zeros are allowed"),
            ("4-+3-+0", [1], "Single zeros are allowed"),
        ]

        invalid_cases = [
            ("14+6/03", [], "No leading zeros allowed"),
            ("5*6/-05", [], "No leading zeros allowed"),
            ("4+8+045", [], "No leading zeros allowed"),
            ("7+-+053", [], "No leading zeros allowed"),
        ]

        # Run the tests
        for case in valid_cases:
            self.assertEqual(solver.solve(case[0]), case[1], case[2])

        for case in invalid_cases:
            self.assertEqual(solver.solve(case[0]), case[1], case[2])

    def test_nerdle(self):
        """Tests cases configured for the Nerdle game"""

        # Define the configuration parameters
        config = {
            "allow_consecutive_sum_and_sub_operators": True,
            "allow_leading_zeros": True,
        }

        # Instantiate the solver
        solver = ExpressionSolver(config)

        # Define cases
        valid_cases = [
            ("7+12/01", [19], "Leading 0s are allowed here"),
            ("4-2/-01", [6], "Leading 'negative' 0s are allowed here"),
        ]

        # Run the tests
        for case in valid_cases:
            self.assertEqual(solver.solve(case[0]), case[1], case[2])


if __name__ == "__main__":
    unittest.main()
