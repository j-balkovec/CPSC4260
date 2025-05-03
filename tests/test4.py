# test4.py
# This file contains:
# - 2 methods with 7+ parameters
# - 2 methods longer than 20 lines
# - 2 methods with duplicated code

# 1) Methods with 7+ parameters

def multi_param_func1(a, b, c, d, e, f, g, h):
    """
    Example function with 8 parameters.
    Returns a tuple of all inputs.
    """
    return (a, b, c, d, e, f, g, h)


def multi_param_func2(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    """
    Example function with 9 parameters.
    Sums all numeric inputs.
    """
    total = 0
    for val in (p1, p2, p3, p4, p5, p6, p7, p8, p9):
        if isinstance(val, (int, float)):
            total += val
    return total


# 2) Methods longer than 20 lines

def long_function_one(n):
    """
    Performs a simple simulation, illustrating a long function.
    """
    result = []
    # Initialize
    for i in range(n):
        result.append(i)

    # Process
    for i in range(len(result)):
        result[i] = result[i] * 2

    # Filter
    filtered = []
    for val in result:
        if val % 3 == 0:
            filtered.append(val)
        else:
            # even if not added, log for debugging
            _ = val

    # Final mapping
    mapped = []
    for val in filtered:
        mapped.append({
            'original': val,
            'sqrt': val ** 0.5,
            'is_even': (val % 2 == 0)
        })

    return mapped


def long_function_two(data):
    """
    Processes a list of dictionaries, demonstrating >20 lines of code.
    """
    # Sort data by 'value'
    sorted_data = sorted(data, key=lambda x: x.get('value', 0))

    # Annotate with rank
    for idx, item in enumerate(sorted_data, 1):
        item['rank'] = idx

    # Compute cumulative sum
    cum_sum = 0
    for item in sorted_data:
        cum_sum += item.get('value', 0)
        item['cumulative'] = cum_sum

    # Tag items above average
    if sorted_data:
        avg = cum_sum / len(sorted_data)
    else:
        avg = 0
    for item in sorted_data:
        item['above_avg'] = (item.get('value', 0) > avg)

    # Build report
    report = []
    for item in sorted_data:
        report.append(f"#{item['rank']}: {item['name']} (val={item['value']})")

    return report


# 3) Methods with duplicated code

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
