#Write a Python program that checks if a given character is a vowel or a consonant.
''' if the character containes a,e,i,o,u or A,E,I,O,U they are vowel
if not they are consonat.'''
char=input("enter a character : ")
if char.lower()=='a' or char.lower()=='e' or char.lower()=='i' or char.lower()=='o' or char.lower()=='u':
    print(f'{char} is vowel')
else:
    print(f'{char} is consonant')
