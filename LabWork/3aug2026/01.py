list1=[]
list2=[]
list3=[]
num=input("enter the list values:")
list1=num.split()
for i in list1:
    list2.append(int(i))
lent=len(list2)
s=0
for n in list2:
    s=s+n
avg=s//lent
for r in list2:
    if r>avg:
        list3.append(r)
print(list3)
