def check_if_positive_v1(num):
    """Checks if a number is positive."""
    if not isinstance(num, (int, float)):
        raise TypeError("Input must be a number.")
    return num > 0

def is_greater_than_zero_v1(number):
    """Checks if a number is greater than zero."""
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number.")
    return number > 0