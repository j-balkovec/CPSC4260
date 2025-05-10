def filter_sort_paginate(data, filter_key=None, filter_value=None, sort_key=None, sort_order="asc", page_number=1, page_size=10):
    """
    Filters, sorts, and paginates a list of dictionaries.

    Args:
        data (list): A list of dictionaries.
        filter_key (str, optional): The key to filter by. Defaults to None.
        filter_value (any, optional): The value to filter for. Defaults to None.
        sort_key (str, optional): The key to sort by. Defaults to None.
        sort_order (str, optional): The sorting order ("asc" or "desc"). Defaults to "asc".
        page_number (int, optional): The page number to retrieve (1-based). Defaults to 1.
        page_size (int, optional): The number of items per page. Defaults to 10.

    Returns:
        list: A list of dictionaries representing the requested page of filtered and sorted data.

    Edge Cases:
        - Empty data list returns an empty list.
        - Invalid sort_order defaults to "asc".
        - Non-positive page_number or page_size will return an empty list.
    """
    if not data:
        return []

    filtered_data = data
    if filter_key is not None and filter_value is not None:
        filtered_data = [item for item in data if item.get(filter_key) == filter_value]

    if sort_key is not None:
        reverse = sort_order.lower() == "desc"
        filtered_data.sort(key=lambda item: item.get(sort_key), reverse=reverse)

    if page_number <= 0 or page_size <= 0:
        return []

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return filtered_data[start_index:end_index]