# name: num_4_multiply_two_numbers_a_compute_product_of_two_values_b
# label: 34
# method_tested: refactor_duplicates()
# should_fail: False
def multiply_two_numbers_a(x, y):
    """Multiplies two numbers."""
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Inputs must be numbers.")
    return x * y


def compute_product_of_two_values_b(val1, val2):
    """Computes the product of two values."""
    if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)):
        raise TypeError("Inputs must be numeric.")
    return val1 * val2
