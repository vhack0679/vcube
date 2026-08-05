'''
3. Write a Python program to print the following square pattern.
Input: 5
Output:

* * * * * *
* * * * * *
* * * * * *
* * * * * *
* * * * * *
'''
no_row=int(input("enter the rows"))
row=1
while row<=no_row:
    print('*'*5)
    row=row+1
