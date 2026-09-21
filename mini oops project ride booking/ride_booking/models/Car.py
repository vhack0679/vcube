
from models.Ride import Ride
class Car(Ride):#child class
    def calculate_fare(self): #method
        return self.get_distance() *20
