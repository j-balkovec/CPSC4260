# name: num_4_check_password_complexity
# label: 4
# method_tested: find_long_method()
# should_fail: False
def check_password_complexity(password):
    """
    Checks if a password meets certain complexity requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit

    Handles very short passwords as an edge case.
    """
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True

    if has_upper and has_lower and has_digit:
        return True
    else:
        return False
