list1=[]
list2=[]
num=input("enter the list values:")
list1=num.split()
for i in list1:
    list2.append(int(i))
L_num=0
S_num=list2[0]
for n in list2:
    if n<S_num:
        S_num=n
    else:
        L_num=n
print(L_num-S_num)
        
