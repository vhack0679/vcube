#Write a Python program that determines if a number is positive, negative, or zero
# using only if statements and no elif or else.
num=int(input("Enter a Number :"))
if num>0:
    print(f'{num} is positive')
if num<0:
    print(f'{num} is negative')
if num==0:
    print(f'{num} is zero')
