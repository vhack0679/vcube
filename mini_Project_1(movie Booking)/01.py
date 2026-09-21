num=list(map(int,input("enter the list values:").split()))
list1=[]
for n in num:
    n1=n
    n2=n
    n3=n
    cnt=0
    while n>0:
        n=n//10
        cnt=cnt+1
    if cnt==2:
        rev=0
        while n1>0:
            d=n1%10
            rev=rev*10+d
            n1=n1//10
        list1.append(n3)
        list1.append(rev)
    else:
        pass
        list1.append(n3)
print(list1)
        
        
    
        
        
    
