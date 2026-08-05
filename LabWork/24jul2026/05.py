'''5. Write a Python program to print all numbers between 1 and N whose sum of digits is even using a while loop.
Input: 20
Output:
2 4 6 8 11 13 15 17 19 20
'''
n=int(input("enter the number"))
i=1
while i<=n:
    bkp=i
    s=0
    while bkp>0:
        d=bkp%10
        s=s+d
        bkp=bkp//10
    if s%2==0:
        print(i)
    i=i+1

  
