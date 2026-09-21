'''

Write a Python program using lambda, filter(), and map() to select all even numbers
from a list and then find their cubes. Input: lst = [1, 2, 3, 4, 5, 6, 7, 8] Output: [8, 64, 216, 512]
'''
lst=list(map(int,input("enter the lst val: ").split()))
lst1=list(map(lambda x:x**3, filter(lambda num:num%2==0, lst)))
print(lst1)
