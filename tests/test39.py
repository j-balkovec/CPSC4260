# name: num_9_convert_to_uppercase_v1_make_string_upper_v1
# label: 39
# method_tested: refactor_duplicates()
# should_fail: False
def convert_to_uppercase_v1(text):
    """Converts a string to uppercase."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    return text.upper()

def make_string_upper_v1(input_string):
    """Makes a given string uppercase."""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string.")
    return input_string.upper()