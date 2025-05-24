def calculate_square_v1(number):
    """Calculates the square of a number."""
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number.")
    return number**2


def get_squared_value_v1(value):
    """Gets the squared value of a value."""
    if not isinstance(value, (int, float)):
        raise TypeError("Input must be a number.")
    return value**2


def check_if_positive_v1(num):
    """Checks if a number is positive."""
    if not isinstance(num, (int, float)):
        raise TypeError("Input must be a number.")
    return num > 0


def is_greater_than_zero_v1(number):
    """Checks if a number is greater than zero."""
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number.")
    return number > 0


def process_audio_segment(
    audio_data, start_time, end_time, fade_in=0, fade_out=0, apply_normalization=False
):
    """
    Processes a segment of audio data.

    Args:
        audio_data (bytes or array): The raw audio data.
        start_time (float): The starting time of the segment in seconds.
        end_time (float): The ending time of the segment in seconds.
        fade_in (float, optional): The duration of the fade-in effect in seconds. Defaults to 0.
        fade_out (float, optional): The duration of the fade-out effect in seconds. Defaults to 0.
        apply_normalization (bool, optional): Whether to apply audio normalization. Defaults to False.

    Returns:
        bytes or array: The processed audio segment.

    Edge Cases:
        - Invalid start or end times (e.g., negative, end before start) might return an error or an empty segment.
        - Zero or negative fade durations are handled as no fade.
        - The actual processing of audio data (fading, normalization) is a placeholder here and would require specific audio processing libraries.
    """
    if start_time < 0 or end_time <= start_time:
        return b""  # Or raise an error

    processed_segment = audio_data  # Placeholder for actual segment extraction

    if fade_in > 0:
        # Apply fade-in logic (requires audio processing library)
        pass
    if fade_out > 0:
        # Apply fade-out logic (requires audio processing library)
        pass
    if apply_normalization:
        # Apply normalization logic (requires audio processing library)
        pass

    return processed_segment


def process_data_range(
    data_list, start_index, end_index, default_value=None, error_on_out_of_bounds=False
):
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
            raise IndexError(
                f"Index {i} is out of bounds for list of length {len(data_list)}."
            )
        else:
            results.append(default_value)
    return results


def format_paragraph_with_indentation(paragraph, indent_level=4):
    """
    Formats a paragraph by splitting it into lines and adding a specified
    indentation to each line. Handles empty paragraphs.
    """
    if not paragraph:
        return ""

    lines = paragraph.splitlines()
    indent = " " * indent_level
    formatted_lines = [indent + line for line in lines]

    return "\n".join(formatted_lines)


def format_data_table(data, headers=None, padding=3):
    """
    Formats a list of lists into a simple text-based table with padding.
    Handles empty data and optional headers.
    """
    if not data:
        return ""

    num_cols = len(data[0]) if data else 0
    if headers and len(headers) != num_cols:
        raise ValueError("Number of headers must match the number of columns")

    all_data = [headers] + data if headers else data
    col_widths = [max(len(str(item)) for item in col) for col in zip(*all_data)]

    separator = "--" * (sum(col_widths) + padding * num_cols) + "-"

    formatted_table = separator + "\n"
    for row in all_data:
        formatted_row = " | ".join(
            str(item).ljust(col_widths[i]) for i, item in enumerate(row)
        )
        formatted_table += formatted_row + " |\n"
    formatted_table += separator

    return formatted_table


x = 5
y = 10
z = 15
a = 20
b = 25
c = 30

d = x + y + z + a + b + c
