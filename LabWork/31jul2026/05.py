list1=[]
list2=[]
while True:
    num=int(input("enter the number:"))
    if num==0:
        break
    else:
        list1.append(num)
for n in list1:
    bkp_n=n
    rev=0
    while n >0:
        d=n%10
        rev=rev*10+d
        n=n//10
    s=rev+bkp_n
    s1=s
    rev1=0
    while s>0:
        k=s%10
        rev1=rev1*10+k
        s=s//10
    if rev1==s1:
        list2.append(bkp_n)
print(list2)
        
    
    
