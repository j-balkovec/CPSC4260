# Duplicated Code Guide  
**Jakob Balkovec**

In software, duplicated code is one of the most common "code smells." It makes your codebase harder to maintain, debug, and refactor.

---

## **Type 1: Exact Duplicates (Copy-Paste Duplication)**

This is literally the same code block repeated in more than one place.

```python
def calculate_area1():
    width = 10
    height = 5
    return width * height

def calculate_area2():
    width = 10
    height = 5
    return width * height
```

🧠 **What to do?**
Extract the repeated logic into a shared function and reuse it.

---

## Type 2: Syntactic Duplication (Minor Changes Only)

Same structure, but variable names or literals are slightly different.

```python
def greet_alice():
    name = "Alice"
    print(f"Hello, {name}!")

def greet_bob():
    name = "Bob"
    print(f"Hello, {name}!")
```

🧠 **What to do?**
Parameterize the changing parts:

```python
def greet(name):
    print(f"Hello, {name}!")
```

---

## Type 3: Structural Duplication (Reordered or Slightly Modified)

Mostly similar, but with added/removed/changed lines.

```python
def send_email():
    connect_to_server()
    login()
    send_message()
    logout()

def send_sms():
    connect_to_server()
    send_message()
    logout()
```

🧠 **What to do?**
Extract the shared flow and let the variable part be handled by a passed-in function or flag.

---

## Type 4: Semantic Duplication (Same Purpose, Different Code)

These do the same thing, but the code looks different.

```python
def sum_list1(nums):
    total = 0
    for num in nums:
        total += num
    return total

def sum_list2(nums):
    return sum(nums)
```

🧠 **What to do?**
In general, replace verbose logic with standard library calls when possible.

**Types 1,2 and 3** are usually easy to spot, but **Type 4** can be tricky. It often requires a deeper understanding of the code's purpose and context.

The project only requires the identification and refactoring of the first 3 types of duplication. Type 4 is outside the scope of this class.