'''
8. Write a Python program to find the sum of all factors of a given number.
Input: 12
Output: 28
'''
n=int(input("Enter the number :"))
i=1
Sum=0
while i<=n:
    if n%i==0:
        Sum=Sum+i
    i=i+1
print(Sum)
