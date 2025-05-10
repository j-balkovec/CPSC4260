# name: num_6_display_product_summary_show_order_details_with_shipping
# label: 26
# method_tested: find_duplicated_code()
# should_fail: False
def display_product_summary(product_code, product_name, price):
    """Displays a brief product summary."""
    if not product_code:
        return "Missing Product Code"
    return f"Code: {product_code}, Name: {product_name}, Price: ${price:.2f}"

def show_order_details_with_shipping(order_number, customer, items, total, shipping_address, tracking_number=None):
    """Shows detailed order information including shipping."""
    if not order_number:
        return "Invalid Order Number"
    details = f"Order #: {order_number}, Customer: {customer}, Total: ${total:.2f}, Items: {len(items)}"
    if shipping_address:
        details += f", Ship To: {shipping_address}"
        if tracking_number:
            details += f", Tracking: {tracking_number}"
        else:
            details += ", Awaiting Tracking"
    else:
        details += ", Shipping Address Missing!"
    return details