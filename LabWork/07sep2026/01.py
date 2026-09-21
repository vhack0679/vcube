'''
Write a recursive function flatten(lst) that converts a nested list into a single flat list.
Input: lst = [1, [2, 3], [4, [5, 6]], 7] Output: [1, 2, 3, 4, 5, 6, 7]
'''
output=[]
def flatten(lst):
    global output
    for ele in lst:
        if type(ele)==list:
            flatten(ele)

        else:
            output.append(ele)
    return output
lst = [1, [2, 3], [4, [5, 6]], 7]
res=flatten(lst)
print(res)
        
        
