# 3  Write a Python program to reverse the digits of a given number. Input: 3742 Output: 2473
n=int(input("enter the number :"))
while True:
    num=n%10
    print(num,end='')
    n=n//10
    if n==0:
        break

