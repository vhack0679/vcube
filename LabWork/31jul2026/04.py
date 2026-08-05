list1=[]
lsit2=[]
while True:
    num=int(input("enter the number:"))
    if num==0:
        break
    else:
        list1.append(num)
for i in list1:
    s=0
    for j in range(1,i+1):
        if i%j==0:
            s=s+j
    for k in range(2,s//2+1):
        if s%k==0:
            break
    else:
        lsit2.append(i)
print(lsit2)
        
        
    
    
