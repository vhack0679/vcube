'''
Write a recursive function to find the sum of all even digits in a given
number. Input: n = 583624 Output: 20
'''
def summofevendigits(num):#583624
    if num==0:
        return 0
    d=num%10
    num=num//10
    if d%2==0:
        c=d
    else:
        c=0
    return c+summofevendigits(num)
res=summofevendigits(583624)
print(res)
