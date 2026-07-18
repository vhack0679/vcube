
'''
5.Write a Python program to check whether a number is Prime or not using a while loop.
Input:17
Output: Prime Number'''
n=int(input("Enter The Number"))
i=2
while i<n:
    if n%i==0:
        print(" Not Prime Number")
        break
    i=i+1
else:
    print(" Prime Number") 
    
    
