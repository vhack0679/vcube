'''
Write a generator function that generates the first n prime numbers.
Input: n = 8 Output: 2 3 5 7 11 13 17 19
'''
def genprime(n):
    count=0
    k=2
    while n!=count:
        for i in range(2,(k//2)+1):
            if k%i==0:
                break
        else:
            yield k
            count=count+1
        k=k+1
res=  genprime(8)
for i in res:
    print(i,end=' ')
