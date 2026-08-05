#Write a Python program that checks if a number is divisible by both 2 and 3
num=int(input("enter number:"))
if num%2==0 and num%3==0:
    print(f'{num} is divisible by both 2 and 3')
if num%2!=0 or num%3!=0:
    print(f'{num} is not divisible by both 2 and 3')
