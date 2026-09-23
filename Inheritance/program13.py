# Q13. Create Printer and Scanner classes.
# Create MultifunctionDevice inheriting from both.
# It should support printing and scanning.

class Printer:
    def print_document(self):
        print("Printing document...")


class Scanner:
    def scan_document(self):
        print("Scanning document...")


class MultifunctionDevice(Printer, Scanner):
    def display(self):
        print("Multifunction device supports printing and scanning.")


device = MultifunctionDevice()

device.display()
device.print_document()
device.scan_document()