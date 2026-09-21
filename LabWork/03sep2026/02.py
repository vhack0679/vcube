def fabonacci(num):
    a=0
    b=1
    print(a,end=' ')
    print(b,end=' ')
    count=0
    while count!=num:
        c=a+b
        a=b
        b=c
        count=count+1
        yield c
          
res=fabonacci(7)

for i in res:
    print(i, end=' ')
