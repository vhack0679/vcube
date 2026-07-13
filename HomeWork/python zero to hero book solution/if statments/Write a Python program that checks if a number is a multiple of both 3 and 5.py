#Write a Python program that checks if a number is a multiple of both 3 and 5.
num=int(input("Enter Number:"))
if  num%3==0 and num%5==0:
    print(f'{num} is a multiple of both 3 and 5')
