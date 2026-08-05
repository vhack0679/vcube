list1=[]
num=list(map(int,input("enter the list values:").split()))
for n in num:
    s=0
    for j in range(1,n+1):
        if n%j==0:
            s=s+j
    root=s**(0.5)
    if root*root==s:
        list1.append(n)
    
print(list1)
            
