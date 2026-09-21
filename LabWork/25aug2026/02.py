'''
2. Write a Python program to create a mirror string.
Input : abc
Output : abccba
'''
s=input('enter the string to mirror the string :')
def stringmirror(st):
    return st+st[::-1]
print(stringmirror(s))
