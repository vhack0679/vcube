list1=[]
while True:
    num=int(input("enter the number:"))
    if num==0:
        break
    else:
        list1.append(num)
s=0
for i in list1:
    s=s+i
print(s)

