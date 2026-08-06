text = input("Enter message: ")
shift = int(input("Enter shift value: "))

encrypted = ""

for ch in text:
    if ch.isalpha():
        if ch.isupper():
            encrypted += chr((ord(ch)-65+shift)%26+65)
        else:
            encrypted += chr((ord(ch)-97+shift)%26+97)
    else:
        encrypted += ch

print("Encrypted:", encrypted)

decrypted = ""

for ch in encrypted:
    if ch.isalpha():
        if ch.isupper():
            decrypted += chr((ord(ch)-65-shift)%26+65)
        else:
            decrypted += chr((ord(ch)-97-shift)%26+97)
    else:
        decrypted += ch

print("Decrypted:", decrypted)