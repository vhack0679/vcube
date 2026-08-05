n=int(input("enter the n :"))
for num in range(1,n+1):
    cnt=0
    for i in range(1,num+1):
        if num%i==0:
            cnt=cnt+1
    if cnt==3:
        print(num)
           
            
        

           
            
