class Employee:
    def salary(self):
        print("Basic Salary")
class Developer(Employee):
    def salary(self):
        print("Developer Salary:50000")
class Tester(Employee):
    def salary(self):
        print("Tester Salary:40000")
dev=Developer()
dev.salary()
test=Tester()
test.salary()
