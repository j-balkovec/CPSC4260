def calculate_mortgage_payment(principal, annual_interest_rate, loan_term_years, down_payment=0, property_tax_rate=0, insurance_rate=0):
    """
    Calculates the monthly mortgage payment (principal, interest, property tax, and insurance).

    Args:
        principal (float): The total loan amount.
        annual_interest_rate (float): The annual interest rate (as a decimal).
        loan_term_years (int): The loan term in years.
        down_payment (float, optional): The initial down payment. Defaults to 0.
        property_tax_rate (float, optional): The annual property tax rate (as a decimal). Defaults to 0.
        insurance_rate (float, optional): The annual homeowner's insurance rate (as a decimal). Defaults to 0.

    Returns:
        float: The total monthly mortgage payment.

    Edge Cases:
        - Negative values for principal or loan term will raise a ValueError.
        - Zero interest rate is handled.
    """
    if principal < 0 or loan_term_years < 0:
        raise ValueError("Principal and loan term cannot be negative.")

    loan_amount = principal - down_payment
    monthly_interest_rate = annual_interest_rate / 12
    num_payments = loan_term_years * 12

    if monthly_interest_rate == 0:
        monthly_principal_interest = loan_amount / num_payments
    else:
        monthly_principal_interest = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / \
                                     ((1 + monthly_interest_rate)**num_payments - 1)

    monthly_property_tax = (principal * property_tax_rate) / 12
    monthly_insurance = (principal * insurance_rate) / 12

    total_monthly_payment = monthly_principal_interest + monthly_property_tax + monthly_insurance
    return total_monthly_payment