num=tuple(map(int,input("enter the tuple values :").split()))
num=list(num)
target=int(input("enter the target value: "))
list1=[]
for n in range(0,len(num)):
    for i in range(n+1,len(num)):
        if num[n]+num[i]==target:
            list1.append((num[n],num[i]))
print(list1)
    
    
   
        

        
        
    
