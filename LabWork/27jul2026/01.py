#lcm
num1=int(input("Enter the number 1: "))
num2=int(input("Enter the number 2: "))
i=0
if num1>num2:
    i=num1
else:
    num2>num1
    i=num2
while True:
    if i%num1==0 and i%num2==0:
        print(i)
        break
    i=i+1
