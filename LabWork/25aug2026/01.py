'''
1.Write a Python program to compress a string.
Input : aaabbc
Output : a3b2c1
'''
s=input('enter the string to compress a string :')
def stringcompress(st):
    output=''
    for ch in st:
        if ch not in output:
            output=output+ch+str(st.count(ch))
    return output
print(stringcompress(s))
    
