'''
Write a Python program using lambda and reduce() to find the product of all numbers in a list.
Input: lst = [2, 3, 4, 5] Output: 120
'''
from functools import reduce
lst=list(map(int,input("enrter the list val: ").split()))
lst1=reduce(lambda x,y:x*y,lst)
print(lst1)
