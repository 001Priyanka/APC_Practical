def reverse_string(text):
    reverse = ""

    for ch in text:
        reverse = ch + reverse

    return reverse

print(reverse_string("Python"))