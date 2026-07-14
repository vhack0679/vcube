#Write a Python program that checks if a given year is a leap year.
year=int(input("enter the year "))
if year%4==0 and year%100==0 and year%400==0:
    print(f'{year} is the leap year')
else:
     print(f'{year} is the not leap year')
    
