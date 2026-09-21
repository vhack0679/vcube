'''
Create a class Rectangle with attributes length and breadth.
Create an object and calculate and display the area and perimeter
of the rectangle. Input: length = 10 breadth = 5 Output: Area: 50 Perimeter: 30
'''
class Rectangle:
    def __init__(self,l,b):
        self.length=l
        self.breadth=b
    def area_rectangel(self):
        print("Area:",self.length*self.breadth)
    def area_perimeter(self):
        print("Perimeter:",2*(self.length+self.breadth))
obj1=Rectangle(10,5)
obj1.area_rectangel()
obj1.area_perimeter()
