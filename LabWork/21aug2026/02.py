'''
Write a Python function to find the first character that appears more
than once in a string.
Input: abcaefbd Output: a Explanation: The character a is the first character that appears more than once.
'''
def first_word_find(st):
    first_char=st[0]
    if first_char in st[1:]:
        return first_char


s=input('enter the string :')
print(first_word_find(s))
