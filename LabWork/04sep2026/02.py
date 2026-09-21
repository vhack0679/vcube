'''

Write a recursive function to reverse a given number without using loops
or converting the number into a string. Input: n = 48291 Output: 19284
'''
def revnum(num):
    rev=0
    if num==0:#base
        return 
    d=num%10
    num=num//10
    revnum(num)
    rev=rev*10+d
    
    return rev

res=revnum(48291)
print(res)
