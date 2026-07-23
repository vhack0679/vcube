#5. Write a Python program to count the number of digits that are
#greater than 5 in a given number using a while loop.
#Input: 58392716 Output: 4
num=int(input("enter the number:"))
cnt=0
while num>0:
    d=num%10
    if d>5:
        cnt=cnt+1
    num=num//10
print(cnt)
