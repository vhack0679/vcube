num=list(map(int,input("enter the list values:").split()))
start=0
end=len(num)
mid=(start+end)//2
print(num[0:mid]+ num[len(num):mid-1:-1])
