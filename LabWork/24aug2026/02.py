'''
Write a Python function to return a new string by moving all *uppercase letters* to the beginning,
followed by all *lowercase letters*, while preserving their original order.
Input:
PyThOnProGram
Output:
PTOPGyhnroram
Explanation:
Collect all uppercase letters first, then append all lowercase letters without changing
their relative order.
'''
s=input('enter the string : ')
def UpperFirst(st):
    upperlist=[]
    lowerlist=[]
    for ch in st:
        if ch.isupper():
            upperlist.append(ch)
        else:
            lowerlist.append(ch)
    output=upperlist+lowerlist
    output_string=''.join(output)
    return output_string
res=UpperFirst(s)
print(res)
