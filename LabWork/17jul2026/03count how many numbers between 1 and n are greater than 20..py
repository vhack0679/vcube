'''
3. Write a program to count how many numbers between 1 and n are greater than 20.
Input:
25
Output:
5
Explanation:
The numbers are 21, 22, 23, 24, and 25.
'''
n=int(input("Enter the number : "))
count=0
i=1
while i<=n:
    if i>20:
        
        count=count+1
    i=i+1
print(count)
