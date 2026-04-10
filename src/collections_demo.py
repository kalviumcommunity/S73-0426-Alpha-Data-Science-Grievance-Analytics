# Python Collections Demonstration

# -------------------------------
# LIST (Mutable)
# -------------------------------

numbers = [10, 20, 30]

print("Original list:", numbers)

# Access element
print("First element:", numbers[0])

# Modify list
numbers.append(40)
numbers[1] = 25

print("Modified list:", numbers)

# -------------------------------
# TUPLE (Immutable)
# -------------------------------

coordinates = (5, 10, 15)

print("Tuple:", coordinates)

# Access element
print("Second element:", coordinates[1])

# Trying to modify (will cause error if uncommented)
# coordinates[1] = 20

print("Tuples are immutable (cannot be changed)")

# -------------------------------
# DICTIONARY (Key-Value)
# -------------------------------

student = {
    "name": "Vraj",
    "age": 20,
    "course": "Data Science"
}

print("Student Dictionary:", student)

# Access using key
print("Name:", student["name"])

# Modify value
student["age"] = 21

print("Updated Dictionary:", student)