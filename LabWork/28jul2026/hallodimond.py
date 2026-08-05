rows=int(input("enter the nub of rows:"))
if rows%2!=0:
    row_no=1
    mid=rows//2+1
    while row_no<=rows:
        if row_no==1 or row_no==rows:
            print(' '*abs((mid-row_no)), '*', sep='')
        elif row_no<=mid:
            print(' '*(mid-row_no),'*',' '*(2*row_no-3),'*',sep='')
        else:
            print(' '*(row_no-mid),'*',' '*(2*rows-2*row_no-1),'*', sep='')
        

        row_no=row_no+1
    
