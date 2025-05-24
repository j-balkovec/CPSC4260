def _common_logic_7179bbcdeff236ba6e1e0edc4fe87440(data_list, expected_length):
    """Checks if a list has a specific length."""
    if not isinstance(data_list, list) or not isinstance(expected_length, int):
        raise TypeError("First argument must be a list, second must be an integer.")
    return len(data_list) == expected_length


def check_list_length_v1(data_list, expected_length):
    return _common_logic_7179bbcdeff236ba6e1e0edc4fe87440(data_list, expected_length)


def verify_array_size_v1(array_data, target_size):
    return _common_logic_7179bbcdeff236ba6e1e0edc4fe87440(array_data, target_size)
