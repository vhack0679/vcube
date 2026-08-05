# Write a Python program that checks if a given number is prime
num=int(input("enter the number :"))
if num<=1:
    print(f'{num} is not a prime number')
else:
    i=2
    while i<num:
        if num%i==0:
            print(f'{num} is not a prime number')
            break
        i=i+1
    else:
        print(f'{num} is a prime number')
            
