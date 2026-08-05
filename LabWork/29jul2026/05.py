rows=int(input("enter the number"))
for row_no in range(1, rows+1):
    for i in range(1,row_no+1):
        print(chr(64+row_no), end='')
        
    print()
