#7. Write a Python program to print all the factors of a given number using a while loop.
'''Input: 24
Output: 1 2 3 4 6 8 12 24'''
n=int(input("Enter the number :"))
i=1
while i<=n:
    if n%i==0:
        print(i)
    i=i+1
