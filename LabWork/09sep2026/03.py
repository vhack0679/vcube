'''
Create a class Employee with attributes name, employee_id, and salary.
Create an object and display the employee details.
Also calculate the salary after adding a ₹5000 bonus.
Input: name = "Arjun" employee_id = 101 salary = 30000 Output: Name: Arjun Empl
'''
class Employee:
    def __init__(self,n,e_id,s):
        self.name=n
        self.employee_id=e_id
        self.salary=s
    def display(self):
        print('name:',self.name, 'employee_id:',self.employee_id,'salary:',self.salary+5000)
obj1=Employee("Arjun",101,30000)
obj1.display()
