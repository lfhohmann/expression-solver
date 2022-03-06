#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Expressions Solver
------------------

This module validates and solves expressions for games like "Mathler" and "Nerdle".
"""

import re

__author__ = "Lucas Hohmann"
__email__ = "lfhohmann@gmail.com"
__user__ = "@lfhohmann"

__status__ = "Production"
__date__ = "2022/03/06"
__version__ = "2.0.0"
__license__ = "MIT"


# TODO: Implement Unit Tests


class ExpressionSolver:
    """
    Solver class
    ------------

    A class which contains all of the necessary functions to validate and solve
    the passed expression.

    >>> solver = ExpressionSolver()
    ... solver.solve("2-278") -> [276]
    """

    def __init__(self, config: dict) -> None:
        """
        Init object
        -----------

        Initializes the object with the passed config.

        Parameters
        ----------

        #### config : dict (required)

        Dictionary containing the configurations for the rules to validate and
        solve the expression.

        >>> {
        ...  "allow_consecutive_sum_and_sub_operators": True,
        ...  "allow_leading_zeros": False
        ... }

        Returns
        -------

        >>> None
        """

        # Set config
        self.config = config

    def __is_string_a_number(self, string: str) -> bool:
        """
        Check if a string is a number
        --------------

        Checks if a passed string is a number or not.

        Parameters
        ----------

        #### string : str (required)
        String containing the characters to be check

        >>> "-1234" -> True
        >>> "+4321" -> True
        >>> "12.34" -> False
        >>> "123ab" -> False

        Returns
        -------

        #### bool:
        True or False depending on if the string is a number or not

        >>> True
        >>> False
        """

        # Try to convert to a number, if it suceeds it's a number
        try:
            int(string)
            return True

        # If it fails, it's not a number
        except ValueError:
            return False

    def __pre_validate(self, expression: str) -> bool:
        """
        Check if an expression is valid before solving it
        --------------

        Checks if a passed expression as a string is valid or not.

        Parameters
        ----------

        #### expression : str (required)
        String containing the characters of the expression

        >>> "-12+34*2" -> True
        >>> "-+2+3*-3" -> True
        >>> "-1a*2b+6" -> False
        >>> "+/43-432" -> False

        Returns
        -------

        #### bool:
        True or False depending on wheter the string is a number or not

        >>> True
        >>> False
        """

        # Only allow numbers and operators
        if not re.match(r"^[0-9+-/*]*$", expression):
            return False

        # First char can't be a "/" or "*" operator
        if re.findall(r"^[\/,*]", expression):
            return False

        # Last char has to be a number
        if re.findall(r"\D$", expression):
            return False

        # There can't be consecutive "/" or "*" operators
        if re.findall(r"\D[\/,*]", expression):
            return False

        # Check for consecutive "+" and "-" operators depending on config
        elif not self.config["allow_consecutive_sum_and_sub_operators"]:
            if re.findall(r"[+,-]{2}", expression):
                return False

        # Check for leading zeros depending on config
        if not self.config["allow_leading_zeros"]:
            if re.findall(r"0\d", expression):
                return False

        # Expression is valid, return True
        return True

    def __join_numbers(self, expression: list) -> list:
        """
        Join consecutive numbers
        --------------

        Joins consecutive number characters in the expression.

        Parameters
        ----------

        #### expression : list (required)
        List containing the characters of the expression

        >>> ["1", "2", "3", "+", "3", "2", "1"] -> ["123", "+", "321"]
        >>> ["1", "2", "+", "3", "*", "-", "2"] -> ["12", "+", "3", "*", "-", "2"]

        Returns
        -------

        #### list:
        A list containing the joined numbers

        >>> ["123", "+", "321"]
        >>> ["12", "+", "3", "*", "-", "2"]
        """

        # Init temporary string and index number
        temp = ""
        i = 0

        # Loop through the expression
        while i < len(expression):

            # Check if the current element is a number
            if expression[i].isnumeric():

                # Add the number to the temporary string and pop it
                temp += expression[i]
                expression.pop(i)

            # Insert temp into expression if it's not empty
            else:
                if temp != "":
                    expression.insert(i, temp)

                # Reset temp and go to the next element
                temp = ""
                i += 1

        # Append the last temp to the expression
        expression.append(temp)

        # Return the expression
        return expression

    def __join_operators(self, expression: list) -> list:
        """
        Join "+" and "-" operators
        --------------

        Joins consecutive "+" and "-" operators in the expression.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> ["123", "+",  "-", "321"] -> ["123", "-", "321"]
        >>> ["12", "+", "3", "*", "-", "-", "2"] -> ["12", "+", "3", "*", "+", "2"]

        Returns
        -------

        #### list:
        A list containing the elements of the expression with the joined
        operators

        >>> ["123", "+", "321"]
        >>> ["12", "+", "3", "*", "-", "2"]
        """

        # Init index
        i = 1

        # Loop through the whole expression
        while True:

            # Check if there are consecutive "+" and "-" operators
            if expression[i - 1] in "+-" and expression[i] in "+-":

                # If so, join the operators
                if expression[i - 1] == expression[i]:
                    expression[i - 1] = "+"

                else:
                    expression[i - 1] = "-"

                # Remove the current element and reset index
                expression.pop(i)
                i = 1

            # Go to next element if current ones are not "+" or "-" operators
            else:
                i += 1

            # Check if we've reached the end of the expression
            if i >= len(expression):
                break

        # Return the expression
        return expression

    def __join_numbers_to_operators(self, expression: list) -> list:
        """
        Join operators to numbers
        --------------

        Joins "+" and "-" operators to their following numbers.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> ["123", "-", "321"] -> ["123", "-321"]
        >>> ["12", "+", "3", "*", "+", "2"] -> ["12", "+3", "*", "+2"]

        Returns
        -------

        #### list:
        A list containing the elements of the expression with the joined
        operators to numbers

        >>> ["123", "-321"]
        >>> ["12", "+3", "*", "+2"]
        """

        # Init index
        i = 1

        # Loop through the expression while there are "+" and/or "-" operators
        while "+" in expression or "-" in expression:

            # Check if previous element is a "+" or "-" operator
            if expression[i - 1] in "+-":

                # If so, join the operator to the current number element, and pop current element
                expression[i - 1] += expression[i]
                expression.pop(i)

            # Go to next element
            i += 1

        # Return the expression
        return expression

    def __convert_numbers_to_ints(self, expression: list) -> list:
        """
        Strings to ints
        --------------

        Converts the numbers from strings into integers.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> ["123", "+0"] -> [123, 0]
        >>> ["12", "3", "*", "2"] -> [12, 3, "*", 2]

        Returns
        -------

        #### list:
        A list containing the elements of the expression with numbers converted
        to integers

        >>> [123, 0]
        >>> [12, 3, "*", 2]
        """

        # Loop through the expression
        for i in range(len(expression)):

            # Check if the current element is a number
            if self.__is_string_a_number(expression[i]):

                # Convert the number to an integer
                expression[i] = int(expression[i])

        # Return the expression
        return expression

    def __check_for_divisions_by_zero(self, expression: list) -> bool:
        """
        Check divisions by zero
        --------------

        Checks if the expression contains divisions by zero.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> [123, "/", 0] -> True
        >>> [12, 3, "*", 2] -> False

        Returns
        -------

        #### bool:
        True if the expression contains divisions by zero, False otherwise

        >>> True
        >>> False
        """

        # Loop through the expression comparing to element at a time
        for i in range(1, len(expression)):

            # Check if the previous element is a division operator and the current element is zero
            if expression[i - 1] == "/" and expression[i] == 0:

                # Return False if there is a division by zero
                return True

        # Return True if there are no divisions by zero
        return False

    def __solve_div_and_mul_operators(self, expression: list) -> list:
        """
        Solve "/" and "*"
        --------------

        Solves division and multiplication operations, it also checks if the
        result of the divisions are integers.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> [4, 124, "/", 2, "*", 4] -> [4, 248]
        >>> [12, 3, "*", 2] -> [12, 6]
        >>> [4, 124, "/", 3, "*", 4] -> []

        Returns
        -------

        #### list:
        A list containing the result of the operations with the elements of
        the expression

        >>> [4, "+", 248]
        >>> [12, 6]
        >>> []
        """

        # Init index
        i = 1

        # Loop through the expression while there are "/" and/or "*" operators
        while "/" in expression or "*" in expression:

            # Check if current element is a division or multiplication operator
            if expression[i] == "/" or expression[i] == "*":

                # Perform the appropriate operation
                if expression[i] == "/":
                    expression[i - 1] /= expression[i + 1]

                    # Check if the division results in an integer
                    if not expression[i - 1] % 1 == 0:
                        return []

                else:
                    expression[i - 1] *= expression[i + 1]

                # Remove the current element and the following element
                for _ in range(2):
                    expression.pop(i)

            # Go to next element
            else:
                i += 1

        # Return the expression
        return expression

    def __sum_elements(self, expression: list) -> list:
        """
        Sum elements
        --------------

        Sums all of the elements in the expression.

        Parameters
        ----------

        #### expression : list (required)
        List containing the elements of the expression

        >>> [4, "+", 248] -> [252]
        >>> [12, 6] -> [18]
        >>> [] -> []

        Returns
        -------

        #### list:
        A list containing the result of the sum of the elements as a single
        number

        >>> [252]
        >>> [18]
        >>> []
        """

        # Return sum only if list is not empty
        if expression:
            return [int(sum(expression))]

        else:
            return []

    def solve(self, expression: str) -> list:
        """
        Solve expression
        --------------

        Validates and solves an expression and returns the solution as a list,
        if invalid returns an empty list.

        Parameters
        ----------

        #### expression : str (required)
        A string representing the expression to be solved

        >>> "4+254/2" -> [131]
        >>> "234/0" -> []

        Returns
        -------

        #### list:
        A list containing the result of the sum of the elements as a single
        number

        >>> [131]
        >>> []
        """

        # Check if the expression is valid
        if not self.__pre_validate(expression):
            return []

        # Split the expression into a list
        expression = list(expression)

        # Perform the following steps on the expression
        expression = self.__join_numbers(expression)
        expression = self.__join_operators(expression)
        expression = self.__join_numbers_to_operators(expression)
        expression = self.__convert_numbers_to_ints(expression)

        # Check if the expression has any divisions by zero
        if self.__check_for_divisions_by_zero(expression):
            return []

        # Perform the following steps on the expression
        expression = self.__solve_div_and_mul_operators(expression)
        expression = self.__sum_elements(expression)

        # Return the solution
        return expression
