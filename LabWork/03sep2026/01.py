def digitofnum(num):
    while num>0:
        d=num%10
        yield d
        num=num//10
res=digitofnum(54321)
for i in res:
    print(i,end=' ')
