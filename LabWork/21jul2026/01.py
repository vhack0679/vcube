#1. Write a Python program to count the number of even digits in a given number. Input: 4827316 Output: 4
n=int(input("enter the number :"))

cnt=0
while True:
    num=n%10
    if num%2==0:
        cnt=cnt+1
    n=n//10
    if n==0:
        break
print(cnt)
