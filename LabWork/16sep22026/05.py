class Shape:
    def area(self):
        print("Area of Shape")
class Circle(Shape):
    def area(self):
        print("Area of Circle")
class Rectangle(Shape):
    def area(self):
        print("Area of Rectangle")
circle=Circle()
rectangle=Rectangle()
Shapes=[circle,rectangle]
for shape in Shapes:
    shape.area()
        
