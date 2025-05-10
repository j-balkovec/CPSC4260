def _common_logic_6a66bdf324c4e92e0313ab42dc5839ef(val1, val2):
    """Computes the product of two values."""
    if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)):
        raise TypeError('Inputs must be numeric.')
    return val1 * val2

def multiply_two_numbers_a2(x, y):
    return _common_logic_6a66bdf324c4e92e0313ab42dc5839ef(x, y)

def compute_product_of_two_values_b2(val1, val2):
    return _common_logic_6a66bdf324c4e92e0313ab42dc5839ef(val1, val2)