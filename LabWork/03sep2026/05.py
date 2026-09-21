'''

Write a Python generator function that takes a compressed string and yields
each character/group according to its count. Input: a[2]bc[3] Output: a a bc bc bc
'''
def genfun(st):
    group=''
    count=0
    lst=[]
    for i in range(len(st)):
        if st[i].isalpha():
            group=group + st[i]
        elif st[i].isdigit():
            count=count*10+int(st[i])
        elif st[i]==']':
            while count!=0:
                yield group
                count=count-1
            group=''
s='a[2]bc[3]'
res=genfun(s)
for i in res:
    print(i, end=' ')
    
