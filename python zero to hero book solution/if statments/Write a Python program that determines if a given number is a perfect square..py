#Write a Python program that determines if a given number is a perfect square.
num=int(input("Enter Number :"))
if num<0:
    print(f'{num} is a negitive number it  cannot be perfrct squares.')
if num>0:
    i=0
    while i*i<num:
        i+=1
    if i*i==num:
        print(f'{num} is perfect square')
    if i*i!=num:
        print(f'{num} is not a pefect square')
