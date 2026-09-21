'''
Given a list of integers, display the elements whose indexes are both prime numbers
and Fibonacci numbers. Input: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] Output: 20 30 50
'''
lst=list(map(int,input("enter the input values:").split()))
fab=[]
a=0
b=1
c=1
while b<=len(lst):
    fab.append(c)
    c=a+b
    a=b
    b=c
fab=set(fab)
print(fab)
prm=[]
for num in fab:
    for i in range(2,num//2+1):
        if num%i==0:
            break
    else:
        prm.append(num)
prm.remove(1)
print(prm)
for i in prm:
    print(lst[i])
    
    
