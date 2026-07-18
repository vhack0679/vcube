'''
6. Write a Python program to print all Prime Numbers from 1 to N using nested while loops.
Input: 50
Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
'''
n=int(input("Enter a number: "))
i=2
while i<=n:
    j=2
    while j<i:
        if i%j==0:
            break
        j=j+1
    else:
        print(i)
    i=i+1
            
