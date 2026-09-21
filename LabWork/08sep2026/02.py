'''
Write a Python program using lambda and filter() to extract all numbers that are divisible by
both 3 and 5. Input: lst = [10, 15, 20, 30, 45, 50, 60, 72] Output: [15, 30, 45, 60]
'''
lst=list(map(int,input("enter the list val :").split()))
lst1=list(filter(lambda num:num%3==0 and num%5==0,lst))
print(lst1)
