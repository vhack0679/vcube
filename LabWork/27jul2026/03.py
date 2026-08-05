#3. Write a Python program to print the following
#Hollow Right Triangle Star Pattern.
#Input: 5
#Output:
'''
*
**
*  *
*    *
*****
'''
col=int(input("enter the no col:"))
row=1
while row<=col:
    if row==1 or row==col:
        print('*'*(row),sep='')
    else:
        print('*',' '*(row-2),'*',sep='')
    row=row+1
