#Write a Python program that determines if a number is a perfect cube.
num=int(input("Enter a number: "))
i=0
while i*i*i<num:
    i=i+1
if i*i*i==num:
    print(f'{num} is a perfect cube.')
if i*i*i!=num:
    print(f'{num} is not perfect cube.')
    
