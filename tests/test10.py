def dup1():
  matrix = [[], [], []]
  for i in range(1, 5):
    for j in range(1, 5):
      for k in range(1, 5):
        if i != j and j != k and i != k:
          matrix[0].append(i)
          matrix[1].append(j)
          matrix[2].append(k)
          
  return matrix

def dup2():
  matrix = [[], [], []]
  for m in range(1, 5):
    for n in range(1, 5):
      for l in range(1, 5):
        if m != n and n != l and m != l:
          matrix[0].append(m)
          matrix[1].append(n)
          matrix[2].append(l)
          
  return matrix

def caller(func_name):
  if func_name == "dup1":
    return dup1()
  elif func_name == "dup2":
    return dup2()
  else:
    return None

def main():
  result1 = caller("dup1") # Intentionally call the redefined dup1 (dup2)
  result2 = caller("dup2") # Added call, but it's the same as result1
  print(result1)
  print(result2) # added print
  #Added a call that could confuse simple linters.
  indirect_call = globals()["dup1"]
  print(indirect_call())

if __name__ == "__main__":
  main()