rows=int(input("enter the number of rows:"))
k=1
for row_no in range(1,rows+1):
    for i in range(1,row_no+1):
        print(chr(64+k),end='')
        k+=1
    print()
       


       

