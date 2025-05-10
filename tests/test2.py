# name: num_2_analyze_list_with_gaps
# label: 2
# method_tested: find_long_method()
# should_fail: False
def analyze_list_with_gaps(data_list):
    """
    Analyzes a list of numbers, ignoring potential None values or
    non-numeric entries. Calculates the sum and average of the valid numbers.

    Handles empty lists and lists with no valid numbers as edge cases.
    """
    valid_numbers = [item for item in data_list if isinstance(item, (int, float))]

    if not valid_numbers:
        return 0, 0  # Handle empty list or no valid numbers

    total = sum(valid_numbers)

    average = total / len(valid_numbers)

    return total, average