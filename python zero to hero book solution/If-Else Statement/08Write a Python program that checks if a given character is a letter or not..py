#Write a Python program that checks if a given character is a letter or not.
char=input("enter something to check character or not :")
if len(char)==1 and 'A' <=char <='Z' or 'a' <=char <='z':
    print(f'{char} is character')
else:
    print(f'{char} is not character')
