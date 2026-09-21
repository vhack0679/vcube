'''
 3. Write a Python function to return all characters that appear *exactly twice* in a string.
Input:
programming
Output:
r g m
Explanation:
Return all characters whose frequency is exactly 2.
'''
s=input('enter the string :')
def chrfrq2(st):
    output_string=''
    for ch in st:
        cnt=st.count(ch)
        if cnt==2:
            if ch not in output_string:
                output_string=output_string+ch
    return output_string
            
res=chrfrq2(s)
print(res)
