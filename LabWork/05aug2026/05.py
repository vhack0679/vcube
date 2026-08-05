num=list(map(int,input("enter the list values:").split()))
k=int(input("enter the k value:"))
print(num[len(num)-k:len(num)]+num[:k+2])
