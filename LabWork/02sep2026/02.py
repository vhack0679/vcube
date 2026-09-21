'''
Write a Python program using a decorator to count the number of times a function is called.
Input: hello() hello() hello()
Output: Call 1: hello Call 2: hello Call 3: hello
'''
def decorator(fun):
    count=0
    def wrapper():
        nonlocal count
        fun()
        count=count+1
        print('call',count,':hello')
    return wrapper
@decorator
def hello():
    return 
    
hello()
hello()
hello()
