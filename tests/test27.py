# name: num_7_calculate_sum_of_squares_v1_compute_squared_sum_v1
# label: 27
# method_tested: find_duplicated_code()
# should_fail: True
def calculate_sum_of_squares_v1(numbers):
    """Calculates the sum of the squares of numbers in a list (imperative)."""
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")
    total = 0
    for num in numbers:
        if isinstance(num, (int, float)):
            total += num ** 2
    return total

def compute_squared_sum_v1(values):
    """Computes the sum of the squares of values in a sequence (functional)."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("Input must be a list or tuple.")
    return sum(x ** 2 for x in values if isinstance(x, (int, float)))