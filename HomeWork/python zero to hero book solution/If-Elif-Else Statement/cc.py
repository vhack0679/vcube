#1. Write a Python program to determine the *shipping charge* based on the order amount.
''' *Input:* Order Amount = ₹1800
   *Output:* Shipping Charge = ₹50

   *Conditions:*

   * Below ₹500 → ₹100
   * ₹500 to ₹1999 → ₹50
   * ₹2000 and above → Free Shipping

orderamt=int(input("enter the order amount :"))
if orderamt<500:
    print("Shipping Charge = ₹100")
elif orderamt<=1999:
    print("Shipping Charge = ₹50")
else:
    print("Free Shipping")
    
'''
'''
2. Write a Python program to determine the *membership level* based on reward points.
   *Input:* Reward Points = 850
   *Output:* Gold Member

   *Conditions:*

   * Below 200 → Bronze
   * 200 to 499 → Silver
   * 500 to 999 → Gold
   * 1000 and above → Platinum

3.Write a program to calculate the sum of the first N natural numbers using a while loop.
Input:10
Output:55n=int(input("enter a number :"))
Sum=1
i=2
while i<=n:
    Sum=Sum*i

    i=i+1
print(Sum)



4.Write a program to find the product of all odd numbers from 1 to N using a while loop.
Input:10
Output:945
n=int(input("enter the number :"))#10
i=1
prd=1
while i<=n: 
    if i%2!=0:
        prd=prd*i
    i=i+1
print(prd)        
  '''
'''
5.Write a Python program to check whether a number is Prime or not using a while loop.
Input:17
Output: Prime Number

6.write a python program to Print numbers divisible by both 2 and 3 using while loop.
Input:20
Output:6 12 18
'''
n=int(input("enter the number :"))
i=1
while i<=n:
    
    
