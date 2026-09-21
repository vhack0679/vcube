class Employee:
    def __init__(self,s=0):
        self.__salary=s
    def set_salary(self,s):
        self.__salary=s
    def get_salary(self):
        print(self.__salary)
e=Employee()
e.set_salary(45000)
e.get_salary()
