
from models.Ride import Ride
class Bike(Ride):#child class

    
    def calculate_fare(self): #method
       return self.get_distance() *10
       
       