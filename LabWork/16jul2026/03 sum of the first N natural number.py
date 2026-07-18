'''
3.Write a program to calculate the sum of the first N natural numbers using a while loop.
Input:10
Output:55
'''
n=int(input("Enter the Number:"))
Sum=0
i=1
while i<=n:
    Sum=Sum+i
    i=i+1
print(Sum)
