from abc import ABC , abstractmethod
class Ride(ABC):
    
    def __init__(self,d):#construtor
        self.__distance=d
        
    def set_distance(self,d): #setter
        self.__distance=d
        
    def get_distance(self): #getter
        return self.__distance
        
    @abstractmethod
    def calculate_fare(self): #abstract method
        pass
class Car(Ride):#child class
    def calculate_fare(self): #method
        return self.get_distance() *20

class Bike(Ride):#child class

    
    def calculate_fare(self): #method
       return self.get_distance() *10