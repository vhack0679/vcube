'''

Create a class Student with the attributes name, roll_no, and marks.

Create an object and display all the student details. Input: name = "Rahul" roll_no = 101 marks = 85 Output: Name: Rahul Roll No: 101 Marks: 85
'''
class student:
    def __init__(self,n,rno,m):
        self.name=n
        self.roll_no=rno
        self.marks=m
    def info(self):
        print('name=',self.name,'roll_no=',self.roll_no,'marks=',self.marks)
obj1=student("Rahul",101,85)
obj1.info()
