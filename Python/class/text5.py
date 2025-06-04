import sys
import os

class Test:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

    def func1(self, a='hello', b='world'):
        return a + b    

    def func2(self, a= [1,2,3,4,5,6]):
        return [i**2 for i in a]

    def func3(self, a =(1,2,3,45), even = [], flag = False):
        for i in a:
            if i % 2 == 0 and flag:
                even.append(i)

        return even     

    def func4(self, a=[1],b=[2], c=[3], bool = False):
        return a + b + c