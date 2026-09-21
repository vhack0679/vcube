'''
Write a generator function that takes a list and yields an element
only when it is different from the previously yielded element.
Input: nums = [1, 1, 2, 2, 2, 3, 1, 1, 4]
Output: 1 2 3 1 4
'''
def genfun(nums):
    for i in range(len(nums)-1):
        if nums[i]!=nums[i+1]:
            yield nums[i]
    else:
        yield nums[-1]
        
nums=[1, 1, 2, 2, 2, 3, 1, 1, 4]
res =genfun(nums)
for i in res:
    print(i,end=' ')
