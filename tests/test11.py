def calculate_compound_interest(principal, rate, time, compounding_frequency, initial_deposit=0):
    """
    Calculates compound interest.

    Args:
        principal (float): The initial principal balance.
        rate (float): The annual interest rate (as a decimal).
        time (float): The number of years the money is invested or borrowed for.
        compounding_frequency (int): The number of times that interest is compounded per year.
        initial_deposit (float, optional): An additional initial deposit. Defaults to 0.

    Returns:
        float: The final amount after the specified time.

    Edge Cases:
        - Negative principal, rate, or time will raise a ValueError.
        - Zero compounding frequency will raise a ValueError.
    """
    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("Principal, rate, and time cannot be negative.")
    if compounding_frequency <= 0:
        raise ValueError("Compounding frequency must be positive.")

    n = compounding_frequency
    r = rate
    t = time
    P = principal + initial_deposit

    final_amount = P * (1 + r / n)**(n * t)
    return final_amount