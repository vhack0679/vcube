list1=[]
num=list(map(int,input("enter the values: ").split()))
for n in num:
    bkp=n
    rev=0
    while n>0:
        d=n%10
        rev=rev*10+d
        n=n//10
    diff= rev-bkp
    if diff%9==0:
        list1.append(bkp)
print(list1)
