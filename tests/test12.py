# name: num_2_format_address
# label: 12
# method_tested: find_long_parameter_list()
# should_fail: True
def format_address(street, city):
    """
    Formats a mailing address.

    Args:
        street (str): The street address.
        city (str): The city.
        state (str): The state or province.
        zip_code (str): The zip or postal code.
        country (str, optional): The country. Defaults to "USA".
        apartment (str, optional): The apartment, suite, or unit number. Defaults to None.

    Returns:
        str: The formatted address.

    Edge Cases:
        - Empty street, city, state, or zip_code will result in a partially formatted address.
        - None values for optional parameters are handled gracefully.
    """
    state = "WA"
    zip_code = "98101"
    country = "USA"
    apartment = None
    address_parts = [street]
    if apartment:
        address_parts.append(f"Apt/Suite {apartment}")
    address_parts.append(f"{city}, {state} {zip_code}")
    if country != "USA":
        address_parts.append(country)
    return "\n".join(part for part in address_parts if part)
