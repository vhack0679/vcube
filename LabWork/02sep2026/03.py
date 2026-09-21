'''
Write a Python program using a decorator to display a message before adding two numbers.
Input: n1 = 10 n2 = 20 Output: Adding 10 and 20 Sum = 30
'''
def decorator(fun):
    def wrapper(a,b):
        print(f"Adding {a} and {b}",'Sum=',fun(a,b))
    return wrapper

@decorator
def add(n1,n2):
    return n1+n2
n1=int(input("enter the n1 value:"))
n2=int(input("enter the n2 value:"))
add(n1,n2)
