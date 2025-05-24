# name: num_8_find_common_elements_with_whitespace
# label: 8
# method_tested: find_long_method()
# should_fail: True
def find_common_elements_with_whitespace(list1, list2):
    """
    Finds common elements between two lists, ignoring leading/trailing
    whitespace in the elements. Handles empty lists.
    """
    if not list1 or not list2:
        return []

    set1 = {item.strip() for item in list1}
    set2 = {item.strip() for item in list2}

    common_elements = list(set1.intersection(set2))

    return common_elements
