'''
5.Write a Python function to check whether two lists are rotations of each other.
Input:
[1, 2, 3, 4, 5]
[3, 4, 5, 1, 2]
Output:
True
Explanation:
Return True if one list can be obtained by rotating the other; otherwise, return False.
'''
list1=list(map(int,input('enter the list1 values: ').split()))
list2=list(map(int,input('enter the list2 values: ').split()))
if len(list1) == len(list2):
    new_list = list1 + list1

    for i in range(len(list1)):
        if new_list[i:i+len(list1)] == list2:
            print(True)
            break
    else:
        print(False)
else:
    print(False)
