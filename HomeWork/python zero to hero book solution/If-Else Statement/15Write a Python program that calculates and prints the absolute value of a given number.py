#Write a Python program that calculates and prints the absolute value of a given number
num=int(input("enter a number : "))
if num<0 or num>0:
    print(f'absolute value of {num} is {-num}')
elif num==0:
    print(f'absolute value of {num} is {num}')
