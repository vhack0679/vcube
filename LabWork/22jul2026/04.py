
#5. Write a Python program to check whether a given number
#is a Neon Number using a while loop. Input: 9 Output: Neon Number
n=int(input("enter the number: "))
ne=n**2
s=0
while ne>0:
    num=ne%10
    s=s+num
    ne=ne//10
if s==n:
    print("Neon number")
else:
    print("not Neon number")
