# ============================================================
# DCOMP320 - DATA STRUCTURES AND ALGORITHM
# Assignment: Stacks Implementation
# Project: Math Evaluator
# ============================================================


# ============================================================
# STACK CLASS
# ============================================================

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self.items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)


# ============================================================
# OPERATOR FUNCTIONS
# ============================================================

def precedence(operator):
    """
    Return the precedence level of an operator.
    """

    if operator in ("+", "-"):
        return 1

    if operator in ("*", "/"):
        return 2

    if operator == "**":
        return 3

    return 0


def is_right_associative(operator):
    """
    Exponentiation is right-associative.
    Example: 2 ** 3 ** 2 = 2 ** (3 ** 2)
    """
    return operator == "**"


# ============================================================
# TOKENIZER
# ============================================================

def tokenize(expression):
    """
    Convert a mathematical expression into tokens.

    Example:
    3 + 5 * 2

    Becomes:
    ['3', '+', '5', '*', '2']
    """

    tokens = []
    i = 0

    while i < len(expression):

        character = expression[i]

        # Ignore spaces
        if character.isspace():
            i += 1
            continue

        # Read numbers
        if character.isdigit() or character == ".":

            number = ""

            while (
                i < len(expression)
                and (
                    expression[i].isdigit()
                    or expression[i] == "."
                )
            ):
                number += expression[i]
                i += 1

            # Make sure the number is valid
            if number.count(".") > 1:
                raise ValueError(
                    "Invalid number: " + number
                )

            tokens.append(number)
            continue

        # Detect exponent operator **
        if character == "*":

            if (
                i + 1 < len(expression)
                and expression[i + 1] == "*"
            ):
                tokens.append("**")
                i += 2
                continue

            tokens.append("*")
            i += 1
            continue

        # Other operators
        if character in "+-/":

            tokens.append(character)
            i += 1
            continue

        # Parentheses
        if character in "()":

            tokens.append(character)
            i += 1
            continue

        # Invalid character
        raise ValueError(
            "Invalid character found: " + character
        )

    return tokens


# ============================================================
# INFIX TO POSTFIX CONVERSION
# ============================================================

def infix_to_postfix(tokens):
    """
    Convert infix notation into postfix notation
    using a stack.

    Example:

    Infix:
    3 + 5 * 2

    Postfix:
    3 5 2 * +
    """

    output = []
    operator_stack = Stack()

    for token in tokens:

        # If token is a number
        if token.replace(".", "", 1).isdigit():

            output.append(token)

        # Opening parenthesis
        elif token == "(":

            operator_stack.push(token)

        # Closing parenthesis
        elif token == ")":

            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != "("
            ):
                output.append(
                    operator_stack.pop()
                )

            # Check for mismatched parentheses
            if operator_stack.is_empty():

                raise ValueError(
                    "Mismatched parentheses."
                )

            # Remove opening parenthesis
            operator_stack.pop()

        # Operator
        elif token in ("+", "-", "*", "/", "**"):

            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != "("
            ):

                top_operator = operator_stack.peek()

                higher_precedence = (
                    precedence(top_operator)
                    > precedence(token)
                )

                same_precedence = (
                    precedence(top_operator)
                    == precedence(token)
                )

                if (
                    higher_precedence
                    or (
                        same_precedence
                        and not is_right_associative(token)
                    )
                ):
                    output.append(
                        operator_stack.pop()
                    )

                else:
                    break

            operator_stack.push(token)

        else:

            raise ValueError(
                "Unknown token: " + token
            )

    # Move remaining operators into output
    while not operator_stack.is_empty():

        operator = operator_stack.pop()

        if operator in ("(", ")"):

            raise ValueError(
                "Mismatched parentheses."
            )

        output.append(operator)

    return output


# ============================================================
# POSTFIX EVALUATION
# ============================================================

def evaluate_postfix(postfix_tokens):
    """
    Evaluate a postfix expression using a stack.
    """

    value_stack = Stack()

    for token in postfix_tokens:

        # Number
        if token.replace(".", "", 1).isdigit():

            if "." in token:
                value_stack.push(float(token))
            else:
                value_stack.push(int(token))

        # Operator
        else:

            if value_stack.size() < 2:

                raise ValueError(
                    "Invalid mathematical expression."
                )

            # Pop operands from stack
            right = value_stack.pop()
            left = value_stack.pop()

            # Perform calculation
            if token == "+":

                result = left + right

            elif token == "-":

                result = left - right

            elif token == "*":

                result = left * right

            elif token == "/":

                if right == 0:

                    raise ZeroDivisionError(
                        "Division by zero is not allowed."
                    )

                result = left / right

            elif token == "**":

                result = left ** right

            else:

                raise ValueError(
                    "Unsupported operator: " + token
                )

            # Push result back onto stack
            value_stack.push(result)

    # There should be exactly one final result
    if value_stack.size() != 1:

        raise ValueError(
            "Invalid mathematical expression."
        )

    return value_stack.pop()


# ============================================================
# EVALUATE ONE EXPRESSION
# ============================================================

def evaluate_expression(expression):
    """
    Evaluate one mathematical expression.
    """

    # Step 1: Tokenize
    tokens = tokenize(expression)

    # Step 2: Convert infix to postfix
    postfix = infix_to_postfix(tokens)

    # Step 3: Evaluate postfix
    result = evaluate_postfix(postfix)

    return result


# ============================================================
# FORMAT RESULT
# ============================================================

def format_result(result):
    """
    Remove unnecessary .0 from whole numbers.

    Example:
    16.0 becomes 16
    """

    if (
        isinstance(result, float)
        and result.is_integer()
    ):
        return str(int(result))

    return str(result)


# ============================================================
# PROCESS INPUT.TXT AND CREATE OUTPUT.TXT
# ============================================================

def process_file(
    input_file="input.txt",
    output_file="output.txt"
):

    """
    Read mathematical expressions from input.txt,
    evaluate them using stacks,
    and write the results to output.txt.
    """

    try:

        # ----------------------------------------------------
        # READ INPUT FILE
        # ----------------------------------------------------

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

        output_lines = []

        # ----------------------------------------------------
        # PROCESS EACH LINE
        # ----------------------------------------------------

        for line in lines:

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Check if the line is a separator
            if set(line) == {"-"}:

                output_lines.append(line)

            else:

                try:

                    # Evaluate expression
                    result = evaluate_expression(line)

                    # Store result
                    output_lines.append(
                        format_result(result)
                    )

                except Exception as error:

                    output_lines.append(
                        "ERROR: " + str(error)
                    )

        # ----------------------------------------------------
        # WRITE OUTPUT.TXT
        # ----------------------------------------------------

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            for line in output_lines:

                file.write(line + "\n")

        # ====================================================
        # DISPLAY RESULTS IN TERMINAL
        # ====================================================

        print()
        print("=" * 55)
        print("                   MATH EVALUATOR")
        print("=" * 55)

        print()
        print("Input file processed successfully.")
        print(
            "Results have been written to:",
            output_file
        )

        # ----------------------------------------------------
        # DISPLAY INPUT
        # ----------------------------------------------------

        print()
        print("INPUT")
        print("-" * 55)

        for line in lines:

            line = line.strip()

            if line:
                print(line)

        # ----------------------------------------------------
        # DISPLAY OUTPUT
        # ----------------------------------------------------

        print()
        print("OUTPUT")
        print("-" * 55)

        for line in output_lines:

            print(line)

        print("-" * 55)

        print()
        print("Program completed successfully.")
        print()


    except FileNotFoundError:

        print()
        print("=" * 55)
        print("ERROR")
        print("=" * 55)

        print(
            "The file",
            input_file,
            "could not be found."
        )

        print()
        print(
            "Make sure input.txt is in the same "
            "folder as main.py."
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    process_file()