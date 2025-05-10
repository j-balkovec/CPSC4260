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
        formatted_row = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
        formatted_table += formatted_row + " |\n"
    formatted_table += separator

    return formatted_table