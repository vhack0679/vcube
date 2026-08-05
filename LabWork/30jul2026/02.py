n=int(input("enter the n value:"))

for num in range(1,n+1):
    p=1
    bk=num
    while num>0:
        d=num%10
        p=p*d
        num=num//10
    if bk%2==0:
        print(bk)
        
        
