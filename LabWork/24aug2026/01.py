'''
1. Write a Python function to return the *longest word* in a given sentence.
If multiple words have the same maximum length, return the *first* one.
Input:
Python is an amazing programming language
Output:
programming
Explanation:
Find the word with the maximum length. If there is a tie, return the word that appears first
'''
s=input('enter the string :')
def longest_word(st):
    st=st.split()
    string_list=list(st)
    wrd_cnt=0
    word=''
    for wrd in string_list:
        if len(wrd)>wrd_cnt:
            wrd_cnt=len(wrd)
            word=wrd
    print(word)
res=longest_word(s)
