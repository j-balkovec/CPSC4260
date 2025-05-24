# name: num_1_process_data_v1_process_info_v1
# label: 21
# method_tested: find_duplicated_code()
# should_fail: False
def process_data_v1(item_id, value, multiplier=1, offset=0):
    """Processes data by multiplying and adding an offset."""
    if not isinstance(item_id, int) or not isinstance(value, (int, float)):
        raise ValueError("item_id must be an integer and value must be numeric.")
    return (value * multiplier) + offset


def process_info_v1(record_id, amount, factor=1, shift=0):
    """Processes info by multiplying and adding a shift."""
    if not isinstance(record_id, int) or not isinstance(amount, (int, float)):
        raise ValueError("record_id must be an integer and amount must be numeric.")
    return (amount * factor) + shift
