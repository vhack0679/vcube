'''
Write a Python program using a decorator to multiply the return value of a function by 2.
Input: calculate(5) Output: Original Result: 5 Final Result: 10
'''

def decorator(fun):
    def wrapper(n):
        r=fun(n)
        print('orginal result:',r)
        r=r*2
        print('final result:',r)
    return wrapper
@decorator
def multiplyby2(n):
    return n
multiplyby2(5)
