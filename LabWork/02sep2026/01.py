'''
Write a Python program using a decorator to display a message before and after executing the function.
Input: hello batch 89
Output: Function Started hello batch 89 Function Ended
'''
def decorator(func):
    def wrapper():
        print("Function Started")
        func()
        print("Function Ended")
    return wrapper
@decorator
def hello():
    print("hello batch 89")

hello()
