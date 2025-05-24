# name: num_3_format_name_v1_construct_full_name_v1
# label: 33
# method_tested: refactor_duplicates()
# should_fail: False
def format_name_v1(first, last):
    """Formats a full name."""
    if not isinstance(first, str) or not isinstance(last, str):
        raise TypeError("First and last names must be strings.")
    return f"{first.strip()} {last.strip()}"


def construct_full_name_v1(given_name, family_name):
    """Constructs a complete name."""
    if not isinstance(given_name, str) or not isinstance(family_name, str):
        raise TypeError("Given and family names must be strings.")
    return f"{given_name.strip()} {family_name.strip()}"
