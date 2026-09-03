# 29. Write a recursive function to search for an element
#     in a sorted list using binary search.

def binary_search(numbers, low, high, key):
    if low > high:
        return -1

    mid = (low + high) // 2

    if numbers[mid] == key:
        return mid
    elif key < numbers[mid]:
        return binary_search(numbers, low, mid - 1, key)
    else:
        return binary_search(numbers, mid + 1, high, key)

numbers = [10, 20, 30, 40, 50, 60]
key = int(input("Enter element to search: "))

result = binary_search(numbers, 0, len(numbers) - 1, key)

if result == -1:
    print("Element not found")
else:
    print("Element found at index", result)