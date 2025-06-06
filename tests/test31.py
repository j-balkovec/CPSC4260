# name: num_1_calculate_square_v1_get_squared_value_v1
# label: 31
# method_tested: refactor_duplicates()
# should_fail: False
def calculate_square_v1(number):
    """Calculates the square of a number."""
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number.")
    return number**2


def get_squared_value_v1(value):
    """Gets the squared value of a value."""
    if not isinstance(value, (int, float)):
        raise TypeError("Input must be a number.")
    return value**2
