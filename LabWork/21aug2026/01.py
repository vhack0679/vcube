'''
Write a Python function to count the number of words that contain at least two vowels.
Input: Python is easy to learn Output: 2 Explanation: Count the words that contain at least two vowels.
'''
def word_cont(st):
    st=st.split()
    list_str=list(st)
    cnt=0
    for wrd in list_str:
        v_cnt=0
        for ch in wrd:
            if ch in'aeioAEIO':
                v_cnt=v_cnt+1
        if v_cnt>=2:
            cnt=cnt+1
    return cnt
s=input('enter the string : ')
print(word_cont(s))
