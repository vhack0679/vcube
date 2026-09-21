class Bike:
    def move(self):
        print("Bike Moves on two wheels")
class Car:
    def move(self):
        print("Car Moves on four wheels")
def show_movement(vehicle):
    vehicle.move()
bike=Bike()
show_movement(bike)
car=Car()
show_movement(car)
        
