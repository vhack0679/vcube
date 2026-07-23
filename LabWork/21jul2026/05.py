'''

5. Write a Python program to check whether a number is a Spy Number using a while loop. Input: 123 Output: Spy Number Explanation: For 123 Sum = 1 + 2 + 3 = 6 Product = 1 × 2 × 3 = 6 Since the sum and product are equal, the number is a Spy Number.
'''
n=int(input("enter the number :"))
prd=1
Sum=0
while True:
    num=n%10
    Sum=Sum+num
    prd=prd*num
    n=n//10
    if n==0:
        break
if Sum==prd:
    print("Spy Number.")

