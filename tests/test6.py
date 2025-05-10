# name: num_6_convert_list_to_spaced_string
# label: 6
# method_tested: find_long_method()
# should_fail: True
def convert_list_to_spaced_string(data_list, separator="   "):
    """
    Converts a list of items to a string where each item is separated by a
    customizable separator with extra whitespace. Handles empty lists.
    """
    if not data_list:
        return ""

    string_representation = separator.join(map(str, data_list))


    return string_representation