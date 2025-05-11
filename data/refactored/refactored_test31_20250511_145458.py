def _common_logic_41a098d5fa2354477cb3dba32c524f91(number):
    """Calculates the square of a number."""
    if not isinstance(number, (int, float)):
        raise TypeError('Input must be a number.')
    return number ** 2

def calculate_square_v1(number):
    return _common_logic_41a098d5fa2354477cb3dba32c524f91(number)

def get_squared_value_v1(value):
    return _common_logic_41a098d5fa2354477cb3dba32c524f91(value)