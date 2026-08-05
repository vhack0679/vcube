num=list(map(int,input("enter the list numbers: ").split()))
list1=[n**2 for n in num if n%2==0]
print(list1)
