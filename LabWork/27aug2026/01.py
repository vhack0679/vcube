#lcm
a=int(input("enter the number:"))
b=int(input("enter the number:"))
if a>b:
    i=a
else:
    i=b
while True:
    if i%a==0 and i%b==0:
        print(i)
        break
    i=i+1
