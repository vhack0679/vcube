# 2. Write a Python program to print the numbers from 1 to 100 that are prime numbers. Output: 2, 3, 5, 7, 11, ..., 97
n=1
while n<=100:
    i=1
    cnt=0
    while i<=n:
        if n%i==0:
            cnt=cnt+1
        i=i+1
    if cnt==2:
        print(i)

    n=n+1

    
