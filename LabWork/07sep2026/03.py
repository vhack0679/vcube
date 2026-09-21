def fourparts(n):
    p=n//4
    
    while n>p:
        if n>2*p:
            yield p
        else:
            yield n
        n=n-p
num=int(input("enter the value:"))
res=fourparts(num)
for i in res:
    print(i)
            
