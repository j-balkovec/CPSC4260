# name: num_5_filter_and_sort_dictionary
# label: 5
# method_tested: find_long_method()
# should_fail: True
def filter_and_sort_dictionary(input_dict, key_prefix="item"):
    """
    Filters a dictionary to include only items where the key starts with
    the given prefix, and then sorts the resulting items by their values.

    Handles empty dictionaries and dictionaries with no matching keys.
    """
    filtered_items = {k: v for k, v in input_dict.items() if k.startswith(key_prefix)}

    if not filtered_items:
        return []

    sorted_items = sorted(filtered_items.items(), key=lambda item: item[1])

    return sorted_items
