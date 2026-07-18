'''
.write a python program to Print numbers divisible by both 2 and 3 using while loop.
Input:20
Output:6 12 18
'''
n=int(input("enter a number :"))
i=1
while i<=n:
    if i%2==0 and i%3==0:
        print(i)
    i=i+1
