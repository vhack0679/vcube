#4. Write a Python program to find the sum of all even digits and the sum of all
#odd digits in a given number using a while loop.
#Input: 4827316 Output: Sum of even digits: 20 Sum of odd digits: 10
num=int(input("enter the number :"))
even_digits=0
odd_digits=0
while num>0:
    d=num%10
    if d%2==0:
        even_digits=even_digits+d
    else:
        odd_digits=odd_digits+d
    num=num//10
print("Sum of even digits:", even_digits)
print("Sum of odd digits:" ,odd_digits)
        
