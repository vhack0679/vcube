'''
4. Write a program to print all numbers between 1 and n except multiples of 5.
Input:
15
Output:
1 2 3 4 6 7 8 9 11 12 13 14
'''
n=int(input("enter a number :"))
i=1
while i<=n:
    if i%5!=0:
        print(i)
    i=i+1
