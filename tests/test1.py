# name: num_1_process_string_with_whitespace
# label: 1
# method_tested: find_long_method()
# should_fail: False
def process_string_with_whitespace(input_string):
    """
    This function takes a string, removes leading and trailing whitespace,
    splits it into words, and then joins them back with a single space.

    It handles empty strings and strings with only whitespace as edge cases.
    """

    if not input_string:
        return ""  # Handle empty string

    stripped_string = input_string.strip()

    if not stripped_string:
        return ""  # Handle string with only whitespace

    words = stripped_string.split()

    processed_string = " ".join(words)

    return processed_string
