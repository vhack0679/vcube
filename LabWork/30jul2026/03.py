n=int(input("enter the number:"))
for num in range(1,n+1):
    bkp=num
    s=0
    while num>0:
        d=num%10
        s=s+d
        num=num//10
    if bkp%s==0:
        print(bkp)
