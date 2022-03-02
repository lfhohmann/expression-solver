import re


# TODO: Document functions
# TODO: Implement Unit Tests


class ExpressionSolver:
    """Class for solving expressions"""

    def __init__(self, config: dict) -> None:
        """Initializes the class"""

        # Set config
        self.config = config

    def __is_string_a_number(self, string: str) -> bool:
        """Helper function to check if the passed string is a number"""

        # Try to convert to a number, if it suceeds it's a number
        try:
            int(string)
            return True

        # If it fails, it's not a number
        except ValueError:
            return False

    def __pre_validate(self, expression: str) -> bool:
        """Checks if an expression is valid before solving it"""

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
        """Joins numbers in the expression"""

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
        """Joins consecutive "+" and "-" operators in the equation"""

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
        """Joins "+" and "-" operators to their following numbers"""

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

    def __check_for_divisions_by_zero(self, expression: list) -> bool:
        """Checks if an expression contains divisions by zero"""

        # Loop through the expression comparing to element at a time
        for i in range(1, len(expression)):

            # Check if the previous element is a division operator and the current element is zero
            if expression[i - 1] == "/" and expression[i] == 0:

                # Return False if there is a division by zero
                return False

        # Return True if there are no divisions by zero
        return True

    def __convert_numbers_to_ints(self, expression: list) -> list:
        """Converts the numbers from strings into integers"""

        # Loop through the expression
        for i in range(len(expression)):

            # Check if the current element is a number
            if self.__is_string_a_number(expression[i]):

                # Convert the number to an integer
                expression[i] = int(expression[i])

        # Return the expression
        return expression

    def __solve_div_and_mul_operators(self, expression: list) -> list:
        """Solves divisions and multiplications"""

        # Init index
        i = 1

        # Loop through the expression while there are "/" and/or "*" operators
        while "/" in expression or "*" in expression:

            # Check if current element is a division or multiplication operator
            if expression[i] == "/" or expression[i] == "*":

                # Perform the appropriate operation
                if expression[i] == "/":
                    expression[i - 1] /= expression[i + 1]

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
        """Sums all of the elements in the expression"""

        return [int(sum(expression))]

    def solve(self, expression: str) -> list:
        """Solves an expression and returns the solution as a list, if invalid returns an empty list"""

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
        if not self.__check_for_divisions_by_zero(expression):
            return []

        # Perform the following steps on the expression
        expression = self.__solve_div_and_mul_operators(expression)
        expression = self.__sum_elements(expression)

        # Return the solution
        return expression
