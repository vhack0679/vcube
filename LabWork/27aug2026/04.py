middel=int(input("Enter the number:"))
if middel%2==0:
    print("enter only odd numbers")
else:
    row_no=1
    while row_no<=(2*middel+1):#1<=6 t
        if row_no<=middel:#1
            print('*'*(row_no))
        else:
            print('*'*((2*middel-1+3)-row_no))
        row_no=row_no+1
            
        
