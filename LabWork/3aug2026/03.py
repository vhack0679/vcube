list1=[]
list2=[]
list3=[]
num=input("enter the list values:")
list1=num.split()
for i in list1:
    list2.append(int(i))
for n in list2:
    bkp=n
    s=0
    p=1
    while n>0:
        d=n%10
        s=s+d
        p=p*d
        n=n//10
    if s>p:
        list3.append(bkp)
print(list3)
