'''

1. Write a Python program to check whether a given number is a perfect cube or not.
Input:27
Output: Perfect Cube
'''
n=int(input("Enter a number :"))
i=0
while i*i*i<n:
    i=i+1
if i*i*i==n:
    print("Perfect Cube")
if i*i*i!=n:
    print("Not Perfect Cube")
