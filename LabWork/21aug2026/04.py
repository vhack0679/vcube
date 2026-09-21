'''
4.Write a Python function to create a new dictionary by assigning a rank to each key based on its value in descending order. The highest value should get rank 1.
Input:
{A: 85, B: 92, C: 78, D: 88}
Output:
{'B': 1, 'D': 2, 'A': 3, 'C': 4}
Explanation:
Assign ranks based on the values in descending order. The key with the highest value gets rank 1, the next highest gets rank 2, and so on.
'''
d=dict(map(lambda x:x.split(':'),input().split(',')))
list1=[]
for keys, values in d.items():
    list1.append((keys,values))
for i in range(len(list1)):
    for j in range(i + 1, len(list1)):
        if int(list1[i][1]) < int(list1[j][1]):
            list1[i], list1[j] = list1[j], list1[i]
result = {}
rank = 1
for keys, values in list1:
    result[keys] = rank
    rank += 1
print(result)


    
