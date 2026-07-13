# singel line comment
# vcube Day01
''' thsi is for multi line comment.
in vcube day 01 i learnd  what is problem solving?
how to solve a proble and after that in pythonabout comments,varibles,data types
'''
'''
a=10 # here a is variable we use variable to store a value and variables are  buliding blocks of a progamming
b=20
print(a+b)
'''
#Level 1 — Easy
#problem 1
'''
Store your name, age, and height (in cm) in 3 variables. Print all 3 on separate lines.

Expected output:
Alice
20
165

name=input('enter your name :')
age=int(input('enter your age :'))
height=float(input('enter your height :'))
print(name)
print(age)
print(height)
'''
#problem 2
'''
Take two numbers a = 15 and b = 4. Print their sum, difference, product, and division.

Expected output:
19
11
60
3.75

a=15
b=4
Sum=a+b
Diffrence=a-b
product=a*b
division=a/b
print(Sum)
print(Diffrence)
print(product)
print(division)
'''
#problem 3
'''
Check and print the data type of these 4 values: 42, 3.14, "hello", True

Expected output:
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))    
'''
#problem 4
'''
Create a string s = "Python". Print its length, first character, last character, and the string reversed.

Expected output:
6
P
n
nohtyP

s="python"
print(len(s))
print(s[0])
print(s[-1])
print(s[::-1])
'''
#Level 2 — Medium
#problem 5
'''
Take num = 17. Using only arithmetic operators, print whether it is even or odd (print the remainder when divided by 2).

Expected output:
1
(1 means odd, 0 means even)

num=17
reminder=num%2
print(reminder)
print('1 means odd, 0 menas even')
'''
#problem 6
'''
Swap the values of two variables x = 100 and y = 200 without using a third variable. Print both before and after.

Before: 100 200
After:  200 100

x=100
y=200
print(f"before {x,y}")
x,y=y,x
print(f"after{x,y}")
'''
#problem 7
'''
Take the string " hello world ". Remove extra spaces, convert to uppercase, and replace "WORLD" with "PYTHON". Print the result.

Expected output:
HELLO PYTHON

s=" hello world "
print(s.strip().upper().replace("WORLD", "PYTHON"))
'''
#problem 8
'''

Take a = "5" and b = "3" (both strings). First print what happens when you do a + b directly. Then convert to int and print their actual sum.

String result: 53
Integer sum:   8


a="5"
b="3"
print(f"string result : {a+b}")
print(f"integer sum : {int(a)+int(b)}")
'''
# problem  9
'''
Take a full name like "john doe smith". Split it into words and print the initials in uppercase separated by dots.

name="john doe smith"
word= name.split()
intial=[word[0].upper() for word in word]
print(".".join(intial))
'''
#problem 10
'''
You have 3 test scores: marks1 = 78, marks2 = 92, marks3 = 85. Calculate the average and print a formatted result using an f-string. Round to 2 decimal places.

Expected output:
Average score: 85.00
Highest score: 92
Lowest score:  78
'''
mark1=78
mark2=92
mark3=85
print(f"Average score : {(mark1+mark2+mark3)/3}")
print(f"Highest score: {max(mark1,mark2,mark3)}")
print(f"Lowest score: {min(mark1,mark2,mark3)}")
