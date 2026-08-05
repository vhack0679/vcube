#Write a Python program that checks if a given year is a century year (ending in '00').
year=int(input("Enter the Year"))
if year%100==0:
    print(f'{year} is century year')
    
else:
    print(f'{year} is a not century year')
