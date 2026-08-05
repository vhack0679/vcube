#Write a Python program that checks if a number is positive or non-positive (including zero).
num=int(input("enter the number : "))
if num==0:
    print(f'{num} is Zero')
elif num<0:
    print(f'{num} is non-positive')
else:
    print(f'{num} is positive')
    
