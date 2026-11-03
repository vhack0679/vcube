'''
Write a function is_balanced(n) to check whether the sum of digits in the left half of
a number is equal to the sum of digits in the right half.
For an odd number of digits, ignore the middle digit. Input: n = 123042 Output: Balanced
'''
def is_balanced(n):
    n = str(n)
    mid = len(n) // 2

    if len(n) % 2 == 0:
        left = n[:mid]
        right = n[mid:]
    else:
        left = n[:mid]
        right = n[mid + 1:]

    left_sum = sum(int(digit) for digit in left)
    right_sum = sum(int(digit) for digit in right)

    if left_sum == right_sum:
        return "Balanced"
    else:
        return "Unbalanced"


print(is_balanced(123042))
