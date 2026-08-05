# 3. Write a Python program to reverse a number and
#check whether the reversed number is divisible by 11 using a while loop.
#Input: 121 Output: Divisible by 11
num=int(input("enter the number:"))
rev=0
while num >0:
    d=num%10
    rev=rev*10+d
    num=num//10
if rev%11==0:
    print("Divisible by 11")
else:
    print("Not Divisible by 11")
