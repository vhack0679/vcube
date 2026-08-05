list1=[]
list2=[]
list3=[]
num=input("enter the list values:")
list1=num.split()
for i in list1:
    list2.append(int(i))
for n in list2:
    bkp=n
    cnt=0
    while n>0:
        n=n//10
        cnt=cnt+1
    power=10**(cnt-1)
    f_digit=bkp//power
    l_digit=bkp%10
    if f_digit==l_digit:
        list3.append(bkp)
print(list3)
        
