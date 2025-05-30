def calculate_square_v1(number):
    """Calculates the square of a number."""
    if not isinstance(number, (int, float)):
        raise TypeError('Input must be a number.')
    return number ** 2
calculate_square_v1(4)
calculate_square_v1(5)