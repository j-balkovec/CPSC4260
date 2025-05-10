# name: num_5_format_user_details_short_format_account_info_extended
# label: 25
# method_tested: find_duplicated_code()
# should_fail: True
def format_user_details_short(user_id, username, role):
    """Formats basic user details."""
    if not user_id:
        return "Invalid User ID"
    return f"User ID: {user_id}, Username: {username}, Role: {role}"

def format_account_info_extended(account_number, owner_name, balance, creation_date, last_login):
    """Formats extended account information."""
    if not account_number:
        return "Invalid Account Number"
    info = f"Account: {account_number}, Owner: {owner_name}, Balance: ${balance:.2f}"
    if creation_date:
        info += f", Created: {creation_date}"
    if last_login:
        info += f", Last Login: {last_login}"
    return info