def foo(x, y):
    # shared logic start
    result = x * y
    if result > 100:
        status = 'large'
    else:
        status = 'small'
    message = f"Result is {result}, status: {status}"
    # shared logic end
    return message

def bar(a, b):
    # shared logic start
    result = a * b
    if result > 100:
        status = 'large'
    else:
        status = 'small'
    message = f"Result is {result}, status: {status}"
    # shared logic end
    return message