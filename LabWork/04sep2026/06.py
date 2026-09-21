'''
Write a recursive function to find the nth Fibonacci number. Input: n = 7 Output: 13
'''
def fab(n):
    if n<=1:
        return n
    return fab(n-2)+fab(n-1)
res=fab(7)
print(res)
    
