class Test:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

    def func1(self, a, b):
        return a + b

    def func2(self, a, b):
        return a + b 

    def func3(self, a, b, c, d):
        return a + b 
    
    def func4(self, e, f, g, h):
        return e + f   
    
    def func5(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j])

    def func6(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j])   