# name: num_10_check_list_length_v1_verify_array_size_v1
# label: 40
# method_tested: refactor_duplicates()
# should_fail: False
def check_list_length_v1(data_list, expected_length):
    """Checks if a list has a specific length."""
    if not isinstance(data_list, list) or not isinstance(expected_length, int):
        raise TypeError("First argument must be a list, second must be an integer.")
    return len(data_list) == expected_length


def verify_array_size_v1(array_data, target_size):
    """Verifies if an array has a target size."""
    if not isinstance(array_data, list) or not isinstance(target_size, int):
        raise TypeError("First argument must be a list, second must be an integer.")
    return len(array_data) == target_size
