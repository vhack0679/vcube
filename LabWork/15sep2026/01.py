class Employee:
    def __init__(self,n,s):
        self.name=n
        self.salary=s
class Manager(Employee):
    def __init__(self,n,s,d):
        super().__init__(n,s)
        self.department=d
    def display(self):
        print("Name:",self.name,"Salary:",self.salary,"Department:",self.department)
obj=Manager("Ravi",45000,"IT")
obj.display()
