# Q10. Create Vehicle.
# Derive Car and Bike from Vehicle.
# Create SportsCar from Car and ElectricBike from Bike.
# Demonstrate different inheritance types.

class Vehicle:
    def __init__(self, brand):
        self.brand = brand


class Car(Vehicle):
    def drive(self):
        print(self.brand, "Car is driving.")


class Bike(Vehicle):
    def ride(self):
        print(self.brand, "Bike is riding.")


class SportsCar(Car):
    def turbo(self):
        print("Sports car has turbo mode.")


class ElectricBike(Bike):
    def charge(self):
        print("Electric bike is charging.")


sc = SportsCar("BMW")
eb = ElectricBike("Ola")

sc.drive()
sc.turbo()

eb.ride()
eb.charge()