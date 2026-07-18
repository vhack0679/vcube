'''
5. Write a program to find the sum of numbers that are divisible by 4 between 1 and n.
Input:
12
Output:
24
'''
n=int(input("enter a number :"))
Sum=0
i=1
while i<=n:
    if i%4==0:
        Sum=Sum+i
    i=i+1
print(Sum)
