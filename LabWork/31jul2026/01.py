list1=[]
while True:
    num=int(input("enter the number:"))
    if num==0:
        break
    else:
        list1.append(num)

large=list1[0]
for i in list1:
    if i>large:
        large=i
print(large)
