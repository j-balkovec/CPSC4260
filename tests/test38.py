def add_two_integers_a(int1, int2):
    """Adds two integers."""
    if not isinstance(int1, int) or not isinstance(int2, int):
        raise TypeError("Inputs must be integers.")
    return int1 + int2

def sum_of_two_whole_numbers_b(num1, num2):
    """Calculates the sum of two whole numbers."""
    if not isinstance(num1, int) or not isinstance(num2, int):
        raise TypeError("Inputs must be whole numbers.")
    return num1 + num2