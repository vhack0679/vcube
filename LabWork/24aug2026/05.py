'''
5. Write a Python function to check whether two strings are *rotations* of each other.
Input:
s1 = "rotation"
s2 = "tionrota"
Output:
True*
'''
def isrotations(s1,s2):
    if s1 in s2+s2:
        return True
    else:
        return False
s1=input('enter the string :')
s2=input('enter the another string :')
res=isrotations(s1,s2)
print(res)
