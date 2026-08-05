n=int(input("enter the number :"))
bkp=n
rev=0
while n>0:
    num=n%10
    rev=rev*10+num
    n=n//10 
if rev==bkp:
    print("pailndrom")
else:
    print("not pailndrom")
    

    
