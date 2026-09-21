num=list(map(int,input("enter the list values:").split()))

for n in num:
    if n==0:
        num.remove(n)
        num.append(n)
        
print(num)       
