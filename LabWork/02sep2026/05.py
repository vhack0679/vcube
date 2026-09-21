'''
Write a Python program using two decorators. The first decorator should convert the message to
uppercase, and the second decorator should add !!! at the end.
Input: hello batch 89 Output: HELLO BATCH 89!!!'''
def decorator_upper(fun):
    def wrapper(s):
        st=fun(s)
        return st.upper()
    return wrapper
def decorator_2(fun):
    def wrapper(s):
        st=fun(s)
        return st+'!!!'
    return wrapper
    
@decorator_2
@decorator_upper
def display(s):
    return s
s=input("enter the string :")
print(display(s))
