rows=int(input("enter the number"))
k=1
for row_no in range(1, rows+1):
    for i in range(1,row_no+1):
        print(k,end='')
        k=k+1
        
    print()
