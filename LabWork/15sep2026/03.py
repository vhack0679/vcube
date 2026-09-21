class Student:
    def __init__(self,n):
        self.name=n
class Marks(Student):
    def __init__(self,n,m):
        super().__init__(n)
        self.marks=m
    
class Result(Marks):
    def __init__(self,n,m):
        super().__init__(n,m)
    def display(self):
        if self.marks>=40:
            print("Name:",self.name,"Marks:",self.marks,"Result:Pass")
        else:
            print("Name:",self.name,"Marks:",self.marks,"Result:Fail")
        
obj=Result("Anil",25)
obj.display()
