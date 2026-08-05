#4. Write a Python program to print the following Right Pascal Star Pattern.
'''
Input: 5
Output:
*
**
***
****
*****
****
***
**
*
'''
mid=int(input("enter the mid value:"))
row_no=1
while row_no<=(mid*2)-1:
    if row_no<=mid:
        print('*'*row_no)
    else:
        print('*'*(2*mid-row_no))

    row_no=row_no+1
