# 2. Write a Python program using a while loop to check
#whether a given number is a Happy Number or not.
'''
19 → 1² + 9² = 82
82 → 8² + 2² = 68
68 → 6² + 8² = 100
100 → 1² + 0² + 0² = 1  ,Since the process reaches 1, the number is called a Happy Number.

'''
num=int(input("enter a number :"))
result=0
while True:
    s=0
    while num>0:
        d=num%10
        s=s+d**2
        num=num//10
    num=s
    result=s
    if result==1:
        break
    if result<10:
        break
if result==1:
    print("Happy Number")
else:
    print("Not Happy Number")


    
