from models.Bike import Bike
from models.Car import Car


class RideFactory:

    @staticmethod
    def create_ride(ride_type, distance):
        if ride_type.lower() == "bike":
            return Bike(distance)
        elif ride_type.lower() == "car":
            return Car(distance)
        else:
            return None