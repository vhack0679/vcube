'''
Write a Python function to check whether a string contains all unique characters.
Input: python Output: True Explanation:
Return True if no character appears more than once; otherwise, return False.
'''
def check_unq_chr(st):
    for i in range(0,len(st)):
        if st[i] in st[i+1:]:
            return False
        
    return True
s=input('enter the string :')
print(check_unq_chr(s))
