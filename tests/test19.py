# name: num_9_generate_report
# label: 19
# method_tested: find_long_parameter_list()
# should_fail: False
def generate_report(
    data,
    report_type="summary",
    include_details=False,
    sort_by=None,
    output_format="text",
    filename="report.txt",
):
    """
    Generates a report from a given dataset.

    Args:
        data (list): The data to include in the report.
        report_type (str, optional): The type of report to generate ("summary" or "full"). Defaults to "summary".
        include_details (bool, optional): Whether to include detailed information. Defaults to False.
        sort_by (str, optional): The key to sort the data by. Defaults to None.
        output_format (str, optional): The output format ("text" or "json"). Defaults to "text".
        filename (str, optional): The name of the output file if saving. Defaults to "report.txt".

    Returns:
        str or None: The report content if output_format is "text", or None if saving to a file.

    Edge Cases:
        - Empty data list results in an empty report.
        - Invalid report_type defaults to "summary".
        - Invalid output_format defaults to "text".
    """
    if not data:
        return "No data to generate report."

    report_content = f"Report Type: {report_type.capitalize()}\n"

    if sort_by:
        data.sort(key=lambda item: item.get(sort_by))

    if report_type == "summary":
        report_content += f"Total items: {len(data)}\n"
        # Add more summary information based on data structure
    elif report_type == "full":
        report_content += "Detailed Data:\n"
        for item in data:
            report_content += f"- {item}\n"
    else:
        report_content += "Invalid report type specified.\n"

    if output_format.lower() == "json":
        import json

        try:
            return json.dumps(data, indent=4)
        except TypeError:
            return "Error: Data cannot be serialized to JSON."
    elif output_format.lower() == "text":
        return report_content
    else:
        return "Invalid output format specified."
