# name: num_7_calculate_geometric_mean
# label: 7
# method_tested: find_long_method()
# should_fail: False
def calculate_geometric_mean(number_list):
    """
    Calculates the geometric mean of a list of positive numbers.

    Handles empty lists and lists containing non-positive numbers as edge cases.
    """
    if not number_list:
        return 0

    product = 1
    for num in number_list:
        if num <= 0:
            raise ValueError("List must contain only positive numbers")
        product *= num

    return product ** (1 / len(number_list))
