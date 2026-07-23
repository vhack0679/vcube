# 2. Write a Python program to repeatedly find the sum of the digits of a given number using
#while loop until a single-digit number is obtained. Input: 4589 Output: 8
n=int(input("enter the number: "))
while n>=10:
    s=0
    while n>0:
        num=n%10
        s=s+num
        n=n//10
    n=s
print(s)
    
