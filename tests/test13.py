def process_data_range(data_list, start_index, end_index, default_value=None, error_on_out_of_bounds=False):
    """
    Processes a specific range of elements within a list.

    Args:
        data_list (list): The list to process.
        start_index (int): The starting index (inclusive).
        end_index (int): The ending index (inclusive).
        default_value (any, optional): The value to return for out-of-bounds indices if error_on_out_of_bounds is False. Defaults to None.
        error_on_out_of_bounds (bool, optional): If True, raise IndexError for out-of-bounds indices. Defaults to False.

    Returns:
        list: A new list containing the elements within the specified range.

    Edge Cases:
        - Empty data_list returns an empty list.
        - start_index greater than end_index returns an empty list.
        - Handles out-of-bounds indices based on the error_on_out_of_bounds flag.
    """
    if not data_list:
        return []
    if start_index > end_index:
        return []

    results = []
    for i in range(start_index, end_index + 1):
        if 0 <= i < len(data_list):
            results.append(data_list[i])
        elif error_on_out_of_bounds:
            raise IndexError(f"Index {i} is out of bounds for list of length {len(data_list)}.")
        else:
            results.append(default_value)
    return results