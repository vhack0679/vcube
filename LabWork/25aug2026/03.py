'''
3. Write a Python program to find the longest palindromic substring.
Input : babad
Output : bab

'''
s=input('enter the string to find longest palindromic substring: ')
def longestpalindromicsubstring(st):
    output=''
    for i in range(len(st)):
        for j in range(i+1,len(st)+1):
            sub=sub[i:j]
            if sub==sub[::-1]:
                if len(sub)>len(output):
                    output=sub
    return output
print(longestpalindromicsubstring(s))
