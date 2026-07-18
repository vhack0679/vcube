'''
2. Write a program to calculate the factorial of a number using a while loop.
Input:
5
Output:
120

5
1*2*3*4*5=120
'''
n=int(input("Enter a Number : "))
prd=1
i=1
while i<=n:
    prd=i*prd 
    i=i+1
print(prd)
