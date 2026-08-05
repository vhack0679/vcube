#5.print the below pattern
'''
input: n=5
output:
*****
*   *
*****
*   *
*****
'''
n=int(input("enter the number: "))
row_no=1
mid=n//2+1
if n%2!=0:
    while row_no<=n:
        if row_no==1 or row_no==mid or row_no==n:
            print('*'*n)
        else:
            print('*',' '*(n-2),'*' ,sep='')
        row_no=row_no+1
else:
    print("enter only odd numbers")
