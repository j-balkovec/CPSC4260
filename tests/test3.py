# name: num_3_format_paragraph_with_indentation
# label: 3
# method_tested: find_long_method()
# should_fail: True
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
