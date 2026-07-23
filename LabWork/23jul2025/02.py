#2 2. Write a Python program to count how many even digits and odd digits are present in a given number using a while loop.
#Input: 4827316 Output: Even digits: 4 Odd digits: 3
num=int(input("enter the number :"))
even_cnt=0
odd_cnt=0
while num>0:
    d=num%10
    if d%2==0:
        even_cnt=even_cnt+1
    else:
        odd_cnt=odd_cnt+1
    num=num//10
print("Even digits:",even_cnt)
print("Odd digits:",odd_cnt)
        
