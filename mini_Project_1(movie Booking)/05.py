num=list(map(int,input("enter the list values:").split()))
list1=[n**2 for n in num  if n**2%3==0 and n**2%2!=0]
print(list1)
