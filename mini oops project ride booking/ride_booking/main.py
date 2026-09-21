from models.Customer import Customer
from factory.ride_factory import RideFactory


name = input("Enter customer name: ")
pickup_location = input("Enter pickup location: ")
distance = float(input("Enter distance: "))
ride_type = input("Enter ride type (Bike/Car): ")


# Factory creates the object
ride = RideFactory.create_ride(ride_type, distance)


if ride is None:
    print("Invalid ride type")

else:
    customer = Customer(name, pickup_location)

    fare = ride.calculate_fare()

    print("\n----- Ride Booking Details -----")
    print("Customer:", customer.name)
    print("Pickup Location:", customer.pickup_location)
    print("Ride Type:", ride_type)
    print("Distance:", ride.get_distance(), "km")
    print("Fare: ₹", int(fare))
    print("----Ride booked successfully----")