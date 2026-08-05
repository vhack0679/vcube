num=list(map(int,input("enter the list values :").split()))
start=0
end=len(num)
mid=(start+end)//2
print(num[mid:len(num):]+(num[0:mid]))


