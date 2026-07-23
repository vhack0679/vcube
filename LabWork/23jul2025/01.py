# . Write a Python program to count the frequency of a given digit in a number using a while loop.
#Input:
#Number: 12231321
#Digit: 2
#Output: 4
num=int(input("enter the nymber"))
digit=int(input("enter the digit"))
cnt=0
while num>0:
    t=num%10
    if digit==t:
        cnt=cnt+1
    num=num//10
print(cnt)
        
    
