# Q14. Create Camera and Phone classes.
# Camera provides photograph functionality.
# Phone provides calling functionality.
# Smartphone inherits from both.

class Camera:
    def take_photo(self):
        print("Photo taken successfully.")


class Phone:
    def make_call(self, number):
        print("Calling", number)


class Smartphone(Camera, Phone):
    def use_smartphone(self):
        print("Smartphone is ready.")


phone = Smartphone()

phone.use_smartphone()
phone.take_photo()
phone.make_call("9876543210")