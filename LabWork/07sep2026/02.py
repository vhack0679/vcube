output=[]
def nested_sum(lst):
    global output
    for ele in lst:
        if type(ele)==list:
            nested_sum(ele)
        else:
            output.append(ele)
    return sum(output)
lst = [1, [2, 3], [4, [5, 6]], 7]
res=nested_sum(lst)
print(res)
    
