#Write a Python program to check whether the first digit of a number is equal to the last digit
#using a while loop.
#Input: 74547 Output: Yes
num=int(input("enter the number"))
first=num
last=num%10
while first>=10:
    first=first//10
if first==last:
    print("yes")
else:
    print("no")

    
    
    To execute a block of code repeatedly 
