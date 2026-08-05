rows=int(input("enter the number:"))
for row_no in range(rows,0,-1):
    for i in range(row_no,0,-1):
        print(chr(64+i),end='')
    
    print()
