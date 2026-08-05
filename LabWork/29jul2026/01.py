#01
num=int(input("enter the number: "))
list1=[]
for n in range(2,num+1):
    for i in range(2,n//2+1):
        if n%i==0:
            break
    else:
        if num%n==0:
            list1.append(n)
print(list1[-1])
            
        
