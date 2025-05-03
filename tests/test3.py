# test3.py

# Long Parameter List
def create_user(name, age, address, email, phone, username, password, security_question, security_answer):
    print(f"Creating user {name}")

# Long Method
def process_order(order_id):
    print("Starting order processing...")
    order = {"id": order_id}
    print(f"Order {order_id} fetched.")
    validate = True
    if not validate:
        print("Invalid order.")
        return
    inventory_check = True
    if not inventory_check:
        print("Out of stock.")
        return
    payment_status = "Success"
    if payment_status != "Success":
        print("Payment failed.")
        return
    print("Packing order...") 
    print("Shipping order...")
    print("Order completed.")
    print("Thank you for your order!")
    print("No, seriously, thank you!")
    print("We really appreciate it.")
    print("You have no idea how much.")
    
# Duplicated Code
def calculate_area_of_rectangle(length, width):
    return length * width

def calculate_area_of_square(side):
    return side * side  # Similar logic (multiplication) for area