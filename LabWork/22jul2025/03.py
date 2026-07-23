# Write a Python program to print the Fibonacci
#series up to n terms using a while loop. Input: 8 Output: 0 1 1 2 3 5 8 13
n=int(input("enter the number"))
a=0
b=1
print(a,b,end=" ")
i=1
while i<=n-2:
    c=a+b
    print(c, end=" ")
    a=b
    b=c
    i=i+1
