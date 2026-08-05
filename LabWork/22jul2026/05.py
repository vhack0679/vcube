
#3. Write a Python program to check whether a given number
#is an Armstrong Number using a while loop
#. Input: 153 Output: Armstrong Numbe

num=int(input("enter the number"))
bkp=num
bkp1=num
cnt=0
res=0
while num>0:
    num=num//10
    cnt=cnt+1
while bkp>0:
    d=bkp%10
    res=res+d**cnt
    bkp=bkp//10
if res==bkp1:
    print("Armstrong")
else:
    print("not Armstrong")



