sorted_data = [{'value': 10}, {'value': 20}, {'value': 30}]

cum_sum = 0
avg = 0.0
a = 0
b = 0

def compute_max(data):
    max_value = data[0]
    for item in data:
        if item > max_value:
            max_value = item
    return max_value

def compute_sum(data):
    total = 0
    for item in data:
        total += item
    return total

def compute_average(data):
    total = compute_sum(data)
    return total / len(data)

for item in sorted_data:
    cum_sum += item.get('value', 0)
    item['cumulative'] = cum_sum

for element in sorted_data:
    cum_sum += element.get('value', 0)
    element['cumulative'] = cum_sum

for item in sorted_data:
    item['above_avg'] = (item.get('value', 0) > avg)
report = []

for i in range(10):
    print(i)

for i in range(0, 10):
    print(i)

x = a + b
y = b + a

def greet():
    print("Hello, world!")

def greet_user(name):
    print(f"Hello, {name}!")
