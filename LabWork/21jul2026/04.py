# 4. Write a Python program to find the largest digit in the given number. Input: 23451678 Output: 8
n=int(input("enter the number :"))
cmp=1
while True:
    num=n%10
    if num>cmp:
        cmp=num
    n=n//10
    if n==0:
        break
print(cmp)
