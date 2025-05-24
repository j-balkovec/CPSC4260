# name: num_10_process_text_with_custom_whitespace
# label: 10
# method_tested: find_long_method()
# should_fail: True
def process_text_with_custom_whitespace(
    text, leading_spaces=2, internal_spaces=4, trailing_spaces=1
):
    """
    Adds a custom amount of leading spaces, internal spaces between words,
    and trailing spaces to a given text. Handles empty text.
    """
    if not text:
        return ""

    words = text.split()
    processed_text = (
        (" " * leading_spaces)
        + (" " * internal_spaces).join(words)
        + (" " * trailing_spaces)
    )

    return processed_text
