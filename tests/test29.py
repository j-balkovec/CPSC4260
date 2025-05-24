# name: num_9_process_item_details_a_calculate_final_price_a
# label: 29
# method_tested: find_duplicated_code()
# should_fail: False
def process_item_details_a(item_id, name, price):
    """Processes basic item details."""
    return f"ID: {item_id}, Name: {name}, Price: ${price:.2f}"


def calculate_final_price_a(base_price, discount_rate, tax_rate):
    """Calculates the final price after discount and tax."""
    discount = base_price * discount_rate
    price_after_discount = base_price - discount
    tax = price_after_discount * tax_rate
    final_price = price_after_discount + tax
    return final_price


def process_product_info_b(product_code, description, cost):
    """Processes basic product information."""
    return f"Code: {product_code}, Description: {description}, Cost: ${cost:.2f}"  # Similar to process_item_details_a


def calculate_total_cost_b(initial_cost, reduction_rate, sales_tax):
    """Calculates the total cost after reduction and sales tax."""  # Similar logic to calculate_final_price_a
    reduction = initial_cost * reduction_rate
    price_after_reduction = initial_cost - reduction
    added_tax = price_after_reduction * sales_tax
    total_cost = price_after_reduction + added_tax
    return total_cost
