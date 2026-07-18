n1=int(input("Enter the 1st Number"))
n2=int(input("Enter the 2nd Number"))
n3=int(input("Enter the 3rd Number"))
if n1<n2:
    if n1<n3:
        print(n1)
if n2<n1:
    if n2<n3:
        print(n2)
    else:
        print(n3)
if n3<n2:
    if n3<n1:
        print(n3)
    else:
        print(n1)
        
