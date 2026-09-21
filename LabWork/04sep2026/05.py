'''

Write a recursive function to find the sum of the first n natural numbers.
Input: n = 8 Output: 36
'''
def sumofnaturalnum(n):
    if n==1:
        return 1
    return n+sumofnaturalnum(n-1)
res= sumofnaturalnum(8)
print(res)
