num=int(input("enter the number: "))

for n in range(1,num+1):
    for i in range(2,num//2+1):
        if n%i==0:
            break
    else:
        print(n)
    
    
