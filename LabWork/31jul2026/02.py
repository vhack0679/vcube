list1=[]
list2=[]
while True:
    num=int(input("enter the number:"))
    if num==0:
        break
    else:
        list1.append(num)
for i in range(len(list1)):
    if i%2==0:
        list2.append(list1[i])
print(list2)
