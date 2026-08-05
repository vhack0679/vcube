'''
4. Write a Python program to print the following pattern.
Input: 5
Output:
*****
****
***
**
*
'''
no_row=int(input("enter the rows"))

while no_row>=1:
    print('*'*(no_row))
    no_row=no_row+1
