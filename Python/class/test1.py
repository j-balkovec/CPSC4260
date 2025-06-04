class Test:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

    def __str__(self):
        return "a: {0}, b: {1}, c: {2}".format(self.a, self.b, self.c)
    

    def func1(self, a, b):
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j] += b[i][j]
        return a
    

    def func2(self, a, b):
        if not a:
            return "Error: Matrices cannot be multiplied. One of the matrices is empty."
        
        if not b:
            return "Error: Matrices cannot be multiplied. One of the matrices is empty."
        
        if len(a[0]) != len(b):
            return "Error: Matrices cannot be multiplied. Inner dimensions must match."
        
        result = []
        for _ in range(len(a)):
            row = []
            for _ in range(len(b[0])):
                row.append(0)
            result.append(row)
        
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]
        return result    
    

    def func3(self, a, b):
        














        return a + b
    

if __name__ == "__main__":
    test = Test()
    print(test.func1([[1,2,3],[4,5,6]], [[7,8,9],[10,11,12]]))
    print(test.func2([[1,2,3],[4,5,6]], [[7,8],[9,10],[11,12]]))    