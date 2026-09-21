def outerfun(n):
    
    def innerfun(x):
        sum1=x+n
        return sum1
    return innerfun

n=int(input("enter the n value:"))
x=int(input("enter the x value :"))
cfun=outerfun(x)
res=cfun(n)
print(res)
