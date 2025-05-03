def dup_func1(x, y):
    # shared logic start
    result = x * y
    if result > 100:
        status = 'large'
    else:
        status = 'small'
    message = f"Result is {result}, status: {status}"
    # shared logic end
    return message

def dup_func2(a, b):
    # shared logic start
    result = a * b
    if result > 100:
        status = 'large'
    else:
        status = 'small'
    message = f"Result is {result}, status: {status}"
    # shared logic end
    return message