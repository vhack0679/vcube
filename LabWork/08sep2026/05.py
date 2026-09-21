'''
Write a Python program using lambda and map() to replace every number in a list with its square.
Input: lst = [2, 4, 6, 8, 10] Output: [4, 16, 36, 64, 100]
'''
lst=list(map(int,input("enter the list val: ").split()))
lst1=list(map(lambda num:num**2,lst))
print(lst1)


