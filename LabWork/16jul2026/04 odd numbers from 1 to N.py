'''
4.Write a program to find the product of all odd numbers from 1 to N using a while loop.
Input:10
Output:945
'''
n=int(input("Enter the Number:"))
prd=1
i=1
while i<=n:
    if i%2!=0:
        prd=prd*i
    i=i+1
print(prd)
