def fibonacci(n):
  if n == 0:
    return 0
  if n == 1:
    return 1
  return fibonacci(n - 1) + fibonacci(n - 2)

def fibonacci2(n):
  if n == 0:
    return 0
  if n == 1:
    return 1
  return fibonacci2(n - 1) + fibonacci2(n - 2)