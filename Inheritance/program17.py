# Q17. Create Animal with common attributes and methods.
# Derive Dog, Cat, and Cow.
# Implement their specific sounds and behaviors.

class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name, "is eating.")


class Dog(Animal):
    def sound(self):
        print(self.name, "says Woof!")


class Cat(Animal):
    def sound(self):
        print(self.name, "says Meow!")


class Cow(Animal):
    def sound(self):
        print(self.name, "says Moo!")


dog = Dog("Tommy")
cat = Cat("Kitty")
cow = Cow("Gauri")

dog.eat()
dog.sound()

cat.eat()
cat.sound()

cow.eat()
cow.sound()