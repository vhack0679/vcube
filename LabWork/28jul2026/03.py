num=int(input("enter the number"))

for n in range(1,num+1):
    Sum=0
    for i in range(1,n//2+1):
        if n%i==0:
            Sum=Sum+i
    if Sum==n:
        print(n)
