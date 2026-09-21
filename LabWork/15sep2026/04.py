class Company:
    def company_name(self):
        print("ABC Technologies")
class Developer(Company):
    def display(self):
        print("Role:Developer")

class Tester(Company):
    def display(self):
        print("Role:Tester")
obj1=Developer()
obj1.company_name()
obj1.display()
obj2=Tester()
obj2.company_name()
obj2.display()
