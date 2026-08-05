#Write a Python program to check if a given string is a palindrome.
s=input("enter a string : ")
if s.lower()==s.lower()[::-1]:
    print(f'{s} is palindrome')
else:
    print(f'{s} is not a palindrome')
