#Write a Python program that takes two numbers as input and determines the sign of their difference.
num1=int(input("enter 1st number :"))
num2=int(input("enter 2nd number :"))
r=num1-num2
if r>0:
    print("Positive")
if r<0:
    print("Negitive")
