list1=[]
list2=[]
list3=[]
num=input("enter the list values:")
list1=num.split()
for i in list1:
    list2.append(int(i))
for n in list2:
    bkp=n
    rev=0
    while n>0:
        d=n%10
        rev=rev*10+d
        n=n//10
    if rev%bkp==0:
        list3.append(bkp)
print(list3)
