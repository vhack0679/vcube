num=int(input("enter the number:"))#20
bkp=num
sum1=0 #4
while sum1!=1:
    s=0 
    while num>0:
        d=num%10
        s=s+d**2
        num=num//10
    num=s
    sum1=s
    if s==1:
        print("happy number")
        break

    
        

    

