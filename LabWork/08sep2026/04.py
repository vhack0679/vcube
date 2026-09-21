'''
Create a class Student with the attributes name and marks.
Create an object and display the student's details. Input: name = "Rahul" marks = 85 Output: Name: Rahul Marks: 85
'''
class Student:
    def __init__(self,n,m):
        self.name=n
        self.marks=m
    def display(self):
        print("name=",self.name, "marks=",self.marks)
obj1=Student("Vishal",55)
obj1.display()

