# Q2. Create a base class Vehicle with brand and model.
# Create a derived class Car with fuel_type and price.
# Display details and calculate discounted price.

class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model


class Car(Vehicle):
    def __init__(self, brand, model, fuel_type, price):
        super().__init__(brand, model)
        self.fuel_type = fuel_type
        self.price = price

    def discounted_price(self, discount):
        return self.price - (self.price * discount / 100)

    def display(self):
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Fuel Type:", self.fuel_type)
        print("Price:", self.price)
        print("Price after discount:", self.discounted_price(10))


c = Car("Toyota", "Innova", "Diesel", 2500000)
c.display()