rows=int(input("enter the numbers:"))
for row_no in range(1,rows+1):
    for i in range(1,row_no+1):
        print(i, end=' ')
    print()
