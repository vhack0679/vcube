rows=int(input("enter the number:"))
for row_no in range(rows,0,-1):
    
    for i in range(row_no):
        print(chr(65+i),end='')
        
    print()
