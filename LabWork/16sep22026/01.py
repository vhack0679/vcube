class Vehicle:
    def start(self):
        print("Vehicle is starting")
class Car(Vehicle):
    def start(self):
        print("Car starts with a key")
carobj=Car()
carobj.start()
