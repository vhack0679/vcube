num=list(map(int,input("enter the list values:").split()))
fparts=len(num)//4
sparts=fparts+fparts
tpart=sparts+fparts
fpart=tpart+fparts
print(num[:fparts],num[fparts:sparts],num[sparts:tpart],num[tpart:fpart])
