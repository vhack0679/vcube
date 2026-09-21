'''
4. Write a Python function to return the *first non-repeating character* in a string.
Input:
aabbccddefg
Output:
e
Explanation:
Return the first character whose frequency is 1.
'''
def nonrepeatingchr(st):
    output_string=''
    for ch in st:
        if st.count(ch)==1:
            output_string=output_string+ch
    return output_string[0]
s=input('enter the string :')
res=nonrepeatingchr(s)
print(res)
